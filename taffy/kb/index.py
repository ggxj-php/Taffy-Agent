"""知识库索引：解析 -> 切块 -> 分词 / 向量化 -> 建索引，并把结果缓存到磁盘。

缓存按「单个文件」存，文件没动就直接复用上次的切块、分词和向量，只有新增 /
修改 / 删除的文件才重新处理。

检索走几路，再按名次融合（RRF）：
  · 原查询的词匹配：自建稀疏倒排索引 + numpy 向量化打分，查询词只碰到包含它的那些块，
    7 万块规模下 ~2ms。管精确词——STM32F103、I2C、IEEE754 这种。这一路永远都在，
    同语言的命中靠它。
  · 英文检索词：中文提问先用模型写成一句英文关键词再查一遍（见 translate.py），
    管跨语言——「内存取证」和 "memory forensics" 在词表上零交集，靠这一路才打得到
    英文教材。不用向量模型、不花那份钱。这一路只在英文内容里找（中文块有原查询那一路
    兜着，英文关键词落在它们身上纯是噪声）。
  · 向量：问题和原文都算成语义向量比远近（见 embed.py）。要配 key，配了才有这一路。

任何一路出问题（没配、接口挂了、返回的东西看不懂）都只是少一路，检索照常返回：
英文那路退回原查询，向量那路退回纯词匹配，不影响可用。

对外接口只有 KnowledgeBase.build() 和 KnowledgeBase.search() 两个方法。
"""
import math
import os
import pickle
import re

import numpy as np

from ..config import (
    EMBED_DIM,
    KB_CACHE_PATH,
    KB_CHUNK_OVERLAP,
    KB_CHUNK_SIZE,
    KB_SOURCE_WEIGHTS,
    KB_SPARSE_WEIGHT,
    KB_TRANSLATE_WEIGHT,
    KB_VECTOR_WEIGHT,
    KNOWLEDGE_DIR,
)
from . import embed, loader, translate
from .lexicon import expand

# 缓存结构变了就把版本号加一，旧缓存会自动失效重建
_CACHE_VERSION = 6

# BM25 参数：k1 控制词频饱和，b 控制长度归一化强度
_K1 = 1.5
_B = 0.75
# rank_bm25 的默认值，负 idf 会用 epsilon * 平均 idf 兜底
_EPSILON = 0.25

# 融合检索时，每一路各取这么多候选再排，最后才挑前 top_k 个
_CANDIDATES = 100
# RRF 的平滑常数。越大越不看重名次差异，60 是常用取值。
_RRF_K = 60
# 余弦低于这个值就当没匹配上，别把一堆弱相关的内容硬塞给模型
_VECTOR_MIN = 0.30
# 算向量分数时一次处理多少行。分块是为了别一次多出几百 MB 的临时数组。
_VECTOR_BLOCK = 8192

# 跨语言补进来的词打这个折扣（见 lexicon.py）。比原文分词低一档，是为了让
# 「同语言的命中」优先：中文提问先出中文资料，英文教材作为补充而不是反客为主。
_EXPAND_WEIGHT = 0.6

# 剔掉的功能词。中文部分是常见虚词 / 疑问词，英文部分是最常见的几十个停用词。
# 只收「几乎每块都有、本身不携带主题信息」的词，领域词一个都不要往里放。
_STOPWORDS = frozenset("""
的 地 得 了 着 过 是 在 和 与 及 或 等 就 都 而 也 还 又 很 太 更 最 不 没 无 会 能 要
把 被 给 让 向 从 到 对 为 以 之 其 这 那 哪 个 些 们 吧 呢 吗 啊 呀 哦 嗯 哈
我 你 他 她 它 我们 你们 他们 自己 大家 什么 怎么 怎样 如何 为什么 哪些 哪个 哪些
一个 一些 一下 一样 这种 那种 这里 那里 时候 的话 可以 能够 应该 需要 进行 通过 关于
因为 所以 但是 而且 如果 虽然 然后 就是 不是 没有 还是 只是 已经 一定 可能 或许 大概
上 下 里 中 外 前 后 时 用 做 说 看 想 知道 问题 问 答 请 帮 我 你
a an the of to in is are was were be been being am and or but if then than that this these those
it its as at by for from on with without into onto over under out up down off again further once
not no nor so such too very can could will would shall should may might must
do does did done doing have has had having i you he she we they them him his her their ours your my me us
which who whom whose what when where why how all any both each few more most other some only own same
about above after before during between through
""".split())


# 英文后缀还原表，长的排前面（先试 "ations" 再试 "s"）。只保留最常见的那些，
# 具体用法和边界见 _stem()。
_STEM_RULES = sorted(
    (
        ("ations", ""), ("ically", "ic"), ("ation", ""), ("ities", ""),
        ("sses", "ss"), ("iness", "y"), ("ings", ""), ("edly", ""),
        ("ance", ""), ("ence", ""), ("ness", ""), ("ment", ""), ("less", ""),
        ("able", ""), ("ible", ""), ("ally", ""), ("ing", ""), ("ies", "y"),
        ("ous", ""), ("ive", ""), ("ful", ""), ("ion", ""), ("ity", ""),
        ("est", ""), ("ed", ""), ("ly", ""), ("er", ""),
    ),
    key=lambda rule: -len(rule[0]),
)


def _stem_once(token):
    """砍一次后缀 / 复数，砍不动就原样返回。"""
    for suffix, replacement in _STEM_RULES:
        if token.endswith(suffix):
            stem = token[:len(token) - len(suffix)] + replacement
            if len(stem) >= 4:
                return stem
    # 复数：process 这种以 ss 结尾的不动，免得越砍越短
    if token.endswith("s") and not token.endswith(("ss", "us", "is")) and len(token) - 1 >= 4:
        return token[:-1]
    return token


def _stem(token):
    """英文词干还原：让同一个词的不同词形落到同一个词上。

    教材里同一个概念会以各种词形出现（forensic / forensics、encrypt / encryption /
    encrypted），不还原就是「明明是一个词、字面对不上」，白丢分。中文、数字和缩写
    （i2c、stm32f103）一律不碰——那些本来就没有词形变化。

    规则保守：只砍常见后缀，砍完不足 4 个字符就放弃。不追求语言学上正确——乱砍会把
    本来不相干的词并成一个，比不还原更糟。

    反复砍到砍不动为止，不然词形不同的两个词会停在不同的地方：registers 只砍掉复数
    停在 register，而 register 本身砍成 regist，同一个词反倒对不上（requirements
    这类「复数 + 后缀」的词很常见，所以必须收敛）。
    """
    if len(token) < 5 or not token.isascii() or not token.isalpha():
        return token
    for _ in range(4):
        shorter = _stem_once(token)
        if shorter == token:
            break
        token = shorter
    return token


def _segment(text):
    """切词：jieba 分词 -> 转小写 -> 丢功能词 -> 英文还原词干。jieba 首次调用要建词典
    缓存，所以延迟导入。

    英文必须转小写：教材原文大小写混着来（"The Internet of Things"），不统一的话
    查询里的 internet 和索引里的 Internet 是两个不同的词，跨语言检索全落空。
    """
    import jieba

    tokens = []
    for piece in jieba.lcut(text):
        token = piece.lower()
        if _useful(token):
            tokens.append(_stem(token))
    return tokens


def _query_terms(query):
    """把查询变成 [(词, 权重), ...]。

    原文分词权重 1.0；lexicon 按术语补进来的跨语言词打 _EXPAND_WEIGHT 折——中文
    提问会自动带上英文术语，英文教材才可能被命中（反之亦然）。补进来的词同样要过
    _stem，不然索引里存的是还原过的词，两边对不上。
    """
    terms = {token: 1.0 for token in _segment(query)}
    for token in expand(query):
        token = _stem(token.lower())
        if _useful(token):
            terms.setdefault(token, _EXPAND_WEIGHT)
    return list(terms.items())


def _useful(token):
    """纯标点、空白和功能词都丢掉。

    功能词（的 / 是 / the / of 这类）几乎每块都出现，BM25 算出来的 idf 是负数，
    而负 idf 会被 epsilon * 平均 idf 兜底成**正数**——等于每个块都白拿一份分。
    结果是随便一个毫不相关的块也能排到前面，把真正相关的内容（尤其英文教材）
    挤下去。所以这里直接把它们剔掉，别让它们参与打分。
    """
    if not token.strip() or not any(ch.isalnum() for ch in token):
        return False
    return token not in _STOPWORDS


def _weight_of(rel_path):
    """按来源查加权系数，见 config.KB_SOURCE_WEIGHTS。"""
    key = rel_path.replace("\\", "/").lower()
    for prefix, weight in KB_SOURCE_WEIGHTS:
        if key.startswith(prefix):
            return weight
    return 1.0


# 判断一段是不是中文内容，见 _is_chinese()
_CJK = re.compile(r"[\u3400-\u9fff]")
_LETTER = re.compile(r"[A-Za-z\u3400-\u9fff]")


def _is_chinese(text):
    """这段内容是不是以中文写的（给英文检索那一路挡噪声用）。

    判「有没有中文」不行——英文教材里偶尔也夹着一两个汉字（目录、术语对照），一刀切会
    把整本书挡在英文检索之外。所以看比例：中文字符占「字母」的两成以上才算中文内容。
    """
    letters = len(_LETTER.findall(text))
    return letters >= 20 and len(_CJK.findall(text)) * 5 >= letters


def _split(text, size=KB_CHUNK_SIZE, overlap=KB_CHUNK_OVERLAP):
    """按段落打包成块。单段超长就硬切，相邻块留 overlap 个字符重叠。"""
    paragraphs = [p.strip() for p in text.replace("\r\n", "\n").split("\n") if p.strip()]
    chunks = []
    buffer = ""

    for paragraph in paragraphs:
        # 超长段落：先把攒着的冲掉，再按固定长度硬切
        if len(paragraph) > size:
            if buffer:
                chunks.append(buffer)
                buffer = ""
            start = 0
            while start < len(paragraph):
                chunks.append(paragraph[start:start + size])
                if start + size >= len(paragraph):
                    break
                start += size - overlap
            continue

        if len(buffer) + len(paragraph) + 1 > size:
            chunks.append(buffer)
            buffer = buffer[-overlap:] + "\n" + paragraph if overlap else paragraph
        else:
            buffer = f"{buffer}\n{paragraph}" if buffer else paragraph

    if buffer:
        chunks.append(buffer)
    return [c.strip() for c in chunks if c.strip()]


def _scan():
    """递归找出 knowledge/ 下所有受支持的文档，返回相对路径（排序保证稳定）。"""
    os.makedirs(KNOWLEDGE_DIR, exist_ok=True)
    found = []
    for folder, _, names in os.walk(KNOWLEDGE_DIR):
        for name in names:
            full = os.path.join(folder, name)
            if loader.supported(full):
                found.append(os.path.relpath(full, KNOWLEDGE_DIR))
    return sorted(found)


def _parse(rel_path, full_path, signature, want_vectors):
    """把一个文件解析成块，每块带出处、页码、原文和分词结果。

    want_vectors 为真时顺手把整批块向量化（一个文件一次发完，别按块发）。
    """
    chunks = []
    for text, page in loader.load(full_path):
        for piece in _split(text):
            chunks.append({
                "source": rel_path,
                "page": page,
                "text": piece,
                "tokens": _segment(piece),
            })
    entry = {"signature": list(signature), "chunks": chunks}
    if want_vectors:
        # 顺手归一化并转成 numpy，缓存里存的就是这个二进制数组，不再来回转
        entry["vectors"] = _normalize(embed.embed_texts([c["text"] for c in chunks]))
    return entry


def _read_cache(want_vectors, embed_sig):
    """读缓存。

    换了向量模型（或维度）就把存着的向量全丢掉——旧向量跟新模型不在同一个空间里，
    留着算出来的分数是错的。分块和分词还能继续用，不用重新解析一遍 PDF。
    """
    try:
        with open(KB_CACHE_PATH, "rb") as f:
            cache = pickle.load(f)
    except Exception:
        return {}
    if cache.get("version") != _CACHE_VERSION:
        return {}
    files = cache.get("files", {})
    if want_vectors and cache.get("embed") != embed_sig:
        for entry in files.values():
            entry.pop("vectors", None)
    return files


def _write_cache(files, embed_sig):
    os.makedirs(os.path.dirname(KB_CACHE_PATH), exist_ok=True)
    with open(KB_CACHE_PATH, "wb") as f:
        pickle.dump({"version": _CACHE_VERSION, "embed": embed_sig, "files": files}, f)


def _normalize(rows):
    """按行归一化成单位向量，之后点积就是余弦相似度。零向量保持零，不参与匹配。

    存成 float16：8.5 万块 1024 维就是 174MB，float32 要翻倍。缓存在盘上也一样，
    存 Python 浮点列表的话光这一项就要 800MB，所以一定得是 numpy 数组。
    """
    if not len(rows):
        return np.zeros((0, EMBED_DIM), dtype=np.float16)
    matrix = np.asarray(rows, dtype=np.float32)
    norms = np.linalg.norm(matrix, axis=1, keepdims=True)
    np.divide(matrix, norms, out=matrix, where=norms > 0)
    return matrix.astype(np.float16)


class _SparseIndex:
    """倒排索引 + numpy 向量化 BM25 打分。

    postings[词] = (块下标 int32 数组, 词频 float32 数组)。查询时只累加命中的
    那些块，不再像 BM25Okapi 那样对全部块逐个算一遍。
    """

    def __init__(self, token_lists):
        size = len(token_lists)
        self.size = size
        self.doc_len = np.zeros(size, dtype=np.float32)

        buckets = {}
        for i, tokens in enumerate(token_lists):
            self.doc_len[i] = len(tokens)
            if not tokens:
                continue
            counts = {}
            for token in tokens:
                counts[token] = counts.get(token, 0) + 1
            for term, freq in counts.items():
                buckets.setdefault(term, []).append((i, freq))

        self.avgdl = float(self.doc_len.mean()) if size else 0.0
        self.postings = {}
        doc_freq = {}
        for term, pairs in buckets.items():
            pairs.sort()  # 按下标有序，方便按需取交集 / 局部打分
            arr = np.array(pairs, dtype=np.float32)
            self.postings[term] = (arr[:, 0].astype(np.int32), arr[:, 1])
            doc_freq[term] = len(pairs)

        self.idf = {}
        if size:
            idf_sum = 0.0
            negative = []
            for term, freq in doc_freq.items():
                value = math.log(size - freq + 0.5) - math.log(freq + 0.5)
                self.idf[term] = value
                idf_sum += value
                if value < 0:
                    negative.append(term)
            fallback = _EPSILON * idf_sum / len(self.idf)
            for term in negative:
                self.idf[term] = fallback

    def scores(self, terms, weights):
        """只累加命中查询词的块，返回 float32 分数向量（长度 size）。

        terms 是 [(词, 权重), ...]，权重用来压低跨语言补进来的那些词。
        """
        out = np.zeros(self.size, dtype=np.float32)
        if not self.size:
            return out

        norm = 1.0 - _B + _B * self.doc_len / self.avgdl
        k1 = _K1
        for term, term_weight in terms:
            entry = self.postings.get(term)
            if entry is None:
                continue
            idf = self.idf.get(term, 0.0)
            if idf == 0.0:
                continue
            idx, freq = entry
            out[idx] += term_weight * idf * (freq * (k1 + 1.0)) / (freq + k1 * norm[idx])

        if weights is not None:
            out *= weights
        return out


class _VectorIndex:
    """向量索引：所有块的向量拼成一个大矩阵，检索时跟问题的向量算余弦。

    向量建库时就归一化过了，所以点积就是余弦相似度。矩阵存 float16 省一半内存
    （8.5 万块 × 1024 维约 174MB），算的时候分块升到 float32，避免一次多出
    几百 MB 的临时数组。
    """

    def __init__(self, matrix):
        self.matrix = matrix               # (块数, 维度) float16，已归一化
        self.size = int(matrix.shape[0])

    def scores(self, vector):
        """返回每个块的余弦相似度（float32 向量）。"""
        out = np.zeros(self.size, dtype=np.float32)
        query = np.asarray(vector, dtype=np.float32)
        norm = float(np.linalg.norm(query))
        if not self.size or norm == 0.0:
            return out
        query /= norm
        for start in range(0, self.size, _VECTOR_BLOCK):
            stop = min(start + _VECTOR_BLOCK, self.size)
            out[start:stop] = self.matrix[start:stop].astype(np.float32) @ query
        return out


class KnowledgeBase:
    """多路检索：词匹配（稀疏倒排）+ 英文检索词 + 向量。build() 组装，search() 融合。"""

    def __init__(self):
        self.chunks = []
        self._index = None
        self._weights = None
        self._chinese = None
        self._vector = None
        self.vector_error = ""   # 向量那路出问题就把原因记这儿，检索自动退回词匹配
        self.skipped = []        # 解析失败的文件名，便于排查

    def vector_count(self):
        """向量算好了多少块。0 表示这一路没启用、或者还没建好。"""
        return 0 if self._vector is None else self._vector.size

    def build(self):
        """扫描 knowledge/ 建索引，返回块数。没变的部分走缓存，不重复解析、不重复花钱。"""
        want_vectors = embed.enabled()
        embed_sig = embed.signature() if want_vectors else ""
        cached = _read_cache(want_vectors, embed_sig)
        files = {}
        corpus = []
        weights = []

        for rel_path in _scan():
            full_path = os.path.join(KNOWLEDGE_DIR, rel_path)
            stat = os.stat(full_path)
            signature = (stat.st_mtime, stat.st_size)
            entry = cached.get(rel_path)

            # 文件变了要重来；向量这一路开着但缓存里没有向量，也得重来
            stale = not entry or entry.get("signature") != list(signature)
            if not stale and want_vectors and "vectors" not in entry:
                stale = True

            if stale:
                entry = None
                if want_vectors:
                    try:
                        entry = _parse(rel_path, full_path, signature, True)
                    except Exception as exc:
                        # 向量那路出任何问题都不该让整个知识库不可用：关掉它，退回词匹配
                        self.vector_error = f"{type(exc).__name__}: {exc}"
                        want_vectors = False
                if entry is None:
                    try:
                        entry = _parse(rel_path, full_path, signature, False)
                    except Exception:
                        self.skipped.append(rel_path)
                        continue

            files[rel_path] = entry
            corpus.extend(entry["chunks"])
            # 权重按来源算，不写进缓存，改了 KB_SOURCE_WEIGHTS 立刻生效
            weights.extend([_weight_of(rel_path)] * len(entry["chunks"]))

        self.chunks = corpus
        self._index = _SparseIndex([c["tokens"] for c in corpus]) if corpus else None
        self._weights = np.array(weights, dtype=np.float32) if corpus else None
        self._chinese = np.array([_is_chinese(c["text"]) for c in corpus], dtype=bool)
        # 先把带向量的缓存写到盘上，再从 files 里摘掉拼成矩阵，省得内存里存两份
        _write_cache(files, embed_sig)
        self._vector = self._load_vectors(files) if want_vectors else None
        return len(corpus)

    def _load_vectors(self, files):
        """把各文件的向量按块序拼成一个矩阵。顺序对不齐就返回 None（不启用向量那一路）。"""
        pieces = []
        total = 0
        for rel_path in _scan():
            entry = files.get(rel_path)
            if entry is None:
                return None
            vectors = entry.pop("vectors", None)
            if vectors is None or len(vectors) != len(entry["chunks"]):
                return None
            pieces.append(vectors)
            total += len(vectors)
        if not total or total != len(self.chunks):
            return None

        # 拷进一个大矩阵，拷完立刻把小块放掉，峰值只有「大矩阵 + 一个小块」
        matrix = np.empty((total, EMBED_DIM), dtype=np.float16)
        at = 0
        for index, piece in enumerate(pieces):
            matrix[at:at + len(piece)] = piece
            at += len(piece)
            pieces[index] = None
        return _VectorIndex(matrix)

    def search(self, query, top_k):
        """返回 [(分数, 块), ...]，按相关度从高到低，不相关的直接丢掉。

        原查询那一路永远都在：英文检索和向量都只是往结果里补，不会把同语言的命中
        挤掉。反过来，后两路翻不出来 / 没配 key 的时候就只剩原查询一路，行为跟以前
        一样。
        """
        if self._index is None:
            return []

        routes = [(self._rank_sparse(query), KB_SPARSE_WEIGHT)]
        english = translate.to_english(query)
        if english:
            routes.append((self._rank_english(english), KB_TRANSLATE_WEIGHT))
        if self._vector is not None:
            routes.append((self._rank_vector(query), KB_VECTOR_WEIGHT))

        if len(routes) == 1:
            return [(score, self.chunks[i]) for i, score in routes[0][0][:top_k]]
        return self._fuse(routes, top_k)

    def _top(self, scores, floor):
        """取分数最高的一批，返回 [(块下标, 分数), ...]，从高到低。"""
        keep = min(_CANDIDATES, len(scores))
        if keep <= 0:
            return []
        top = np.argpartition(-scores, keep - 1)[:keep]
        top = top[np.argsort(-scores[top])]
        return [(int(i), float(scores[i])) for i in top if scores[i] > floor]

    def _rank_sparse(self, query):
        """词匹配那路（原查询走这条，按来源加权）。"""
        return self._top(self._index.scores(_query_terms(query), self._weights), 0.0)

    def _rank_english(self, query):
        """英文检索那一路：只在英文内容里找。

        中文块有原查询那一路兜着，英文关键词对它们没有意义——中文资料里混着不少英文
        术语（data、structure、memory 这种），拿英文检索词去打分它们也排得挺靠前，
        同一段内容于是两路各得一次分，把真正的英文教材挤下去。所以这里按 _is_chinese
        把中文块直接清零。
        """
        scores = self._index.scores(_query_terms(query), None)
        scores[self._chinese] = 0.0
        return self._top(scores, 0.0)

    def _rank_vector(self, query):
        """向量那路。

        向量服务挂了、key 填错了、返回的东西看不懂——一律返回空、把原因记下来，
        让检索退回词匹配。知识库检索不该因为这一路出问题就整个用不了。
        """
        try:
            vector = embed.embed_query(query)
        except Exception as exc:
            self.vector_error = f"{type(exc).__name__}: {exc}"
            return []
        return self._top(self._vector.scores(vector), _VECTOR_MIN - 1e-6)

    def _fuse(self, routes, top_k):
        """RRF：每一路各按名次给分再相加。

        用名次而不是原始分，是因为各路的分数量纲根本没法比（词匹配十几到几十分，
        余弦 0~1），直接相加就得反复调系数；换成名次天然可比，也不怕某一路恰好
        分数特别大把其它路整个盖住。

        routes 是 [(名次列表, 权重), ...]；只有一路时名次顺序原样保留。
        """
        fused = {}
        for ranked, weight in routes:
            for rank, (i, _) in enumerate(ranked):
                fused[i] = fused.get(i, 0.0) + weight / (_RRF_K + rank)
        best = sorted(fused.items(), key=lambda kv: -kv[1])[:top_k]
        return [(score, self.chunks[i]) for i, score in best]
