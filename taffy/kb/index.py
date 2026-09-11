"""知识库索引：解析 -> 切块 -> 分词 -> 倒排打分，并把解析结果缓存到磁盘。

缓存按「单个文件」存，文件没动就直接复用上次的切块和分词，只有新增 / 修改 /
删除的文件才重新解析。

检索用自建稀疏倒排索引 + numpy 向量化打分，而不是 rank_bm25 的全量扫描：
查询词只会碰到包含它的那些块，7 万块规模下打分从 ~95ms 降到 ~2ms。

想换成向量检索的话，只需要改这个文件：对外接口只有 KnowledgeBase.build()
和 KnowledgeBase.search() 两个方法。
"""
import math
import os
import pickle

import numpy as np

from ..config import (
    KB_CACHE_PATH,
    KB_CHUNK_OVERLAP,
    KB_CHUNK_SIZE,
    KB_SOURCE_WEIGHTS,
    KNOWLEDGE_DIR,
)
from . import loader

# 缓存结构变了就把版本号加一，旧缓存会自动失效重建
_CACHE_VERSION = 1

# BM25 参数：k1 控制词频饱和，b 控制长度归一化强度
_K1 = 1.5
_B = 0.75
# rank_bm25 的默认值，负 idf 会用 epsilon * 平均 idf 兜底
_EPSILON = 0.25


def _segment(text):
    """中文分词。jieba 首次调用要建词典缓存，所以延迟导入。"""
    import jieba

    return [token for token in jieba.lcut(text) if _useful(token)]


def _useful(token):
    """纯标点和空白没有检索价值，丢掉。"""
    return token.strip() and any(ch.isalnum() for ch in token)


def _weight_of(rel_path):
    """按来源查加权系数，见 config.KB_SOURCE_WEIGHTS。"""
    key = rel_path.replace("\\", "/").lower()
    for prefix, weight in KB_SOURCE_WEIGHTS:
        if key.startswith(prefix):
            return weight
    return 1.0


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


def _parse(rel_path, full_path, signature):
    """把一个文件解析成块，每块带出处、页码、原文和分词结果。"""
    chunks = []
    for text, page in loader.load(full_path):
        for piece in _split(text):
            chunks.append({
                "source": rel_path,
                "page": page,
                "text": piece,
                "tokens": _segment(piece),
            })
    return {"signature": list(signature), "chunks": chunks}


def _read_cache():
    try:
        with open(KB_CACHE_PATH, "rb") as f:
            cache = pickle.load(f)
    except Exception:
        return {}
    if cache.get("version") != _CACHE_VERSION:
        return {}
    return cache.get("files", {})


def _write_cache(files):
    os.makedirs(os.path.dirname(KB_CACHE_PATH), exist_ok=True)
    with open(KB_CACHE_PATH, "wb") as f:
        pickle.dump({"version": _CACHE_VERSION, "files": files}, f)


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

    def scores(self, query_tokens, weights):
        """只累加命中查询词的块，返回 float32 分数向量（长度 size）。"""
        out = np.zeros(self.size, dtype=np.float32)
        if not self.size:
            return out

        norm = 1.0 - _B + _B * self.doc_len / self.avgdl
        k1 = _K1
        for term in query_tokens:
            entry = self.postings.get(term)
            if entry is None:
                continue
            idf = self.idf.get(term, 0.0)
            if idf == 0.0:
                continue
            idx, freq = entry
            out[idx] += idf * (freq * (k1 + 1.0)) / (freq + k1 * norm[idx])

        if weights is not None:
            out *= weights
        return out


class KnowledgeBase:
    """一个倒排索引。build() 负责组装，search() 负责检索。"""

    def __init__(self):
        self.chunks = []
        self._index = None
        self._weights = None
        self.skipped = []  # 解析失败的文件名，便于排查

    def build(self):
        """扫描 knowledge/ 建索引，返回块数。文件没变时会走缓存，不会重复解析。"""
        cached = _read_cache()
        files = {}
        corpus = []
        weights = []

        for rel_path in _scan():
            full_path = os.path.join(KNOWLEDGE_DIR, rel_path)
            stat = os.stat(full_path)
            signature = (stat.st_mtime, stat.st_size)
            entry = cached.get(rel_path)

            if not entry or entry.get("signature") != list(signature):
                try:
                    entry = _parse(rel_path, full_path, signature)
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
        _write_cache(files)
        return len(corpus)

    def search(self, query, top_k):
        """返回 [(分数, 块), ...]，按相关度从高到低，不相关的直接丢掉。"""
        if self._index is None:
            return []
        scores = self._index.scores(_segment(query), self._weights)
        keep = min(top_k, len(scores))
        if keep <= 0:
            return []
        top = np.argpartition(-scores, keep - 1)[:keep]
        top = top[np.argsort(-scores[top])]
        return [(float(scores[i]), self.chunks[i]) for i in top if scores[i] > 0]
