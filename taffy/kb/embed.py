"""向量化：调 OpenAI 兼容的 /embeddings 接口，把文本变成向量。

知识库检索的第二路。词匹配那套（kb/index.py 的 BM25）按字面词查，中文问题跟英文
教材在词表上零交集；向量把不同语言的同义内容映到相近位置，中文提问才搜得到英文书。

模型 / 接口地址 / key 都从 settings 里取，网页后台能改，后台还有个总开关。开关关了、
或者三样没配齐，这一路就不启用，检索自动退回纯词匹配，不会报错。

两处「自动适配」：
  · 一次发几条——接口嫌行多就砍半重发（见 embed_texts）；
  · 一条能有多长——建索引前探一次模型的单条输入上限，反推块长（见 max_input_tokens）。
    第二件事是为了小窗口的向量模型（512 / 256 / 128），块切大了会被静默截断或者 400。
"""
import time
from concurrent.futures import ThreadPoolExecutor

import requests

from .. import settings
from ..config import EMBED_DIM

# 一次请求带多少条。各家的「单次最大行数」不一样：百炼 qwen3.7 系列收 20 行，
# text-embedding-v4 / v3 只收 10 行，v1 / v2 是 25 行。先按 _BATCH_MAX 发，接口嫌多
# 就自动砍半重发（见 embed_texts），砍出来的安全值记在 _batch 里，一个进程只碰一次壁。
_BATCH_MAX = 20
_batch = _BATCH_MAX
# 同时开几个请求。全库 8.5 万块要发 4000 多次请求，串行发太慢；4 路既快又不容易被限流。
_WORKERS = 4
_TIMEOUT = 60
_RETRIES = 3

# ---------- 单条输入上限（自动探测）----------
# 上面那个砍半只管「一次发几条」，不管「一条有多长」。而分块是按字数切的
# （config.KB_CHUNK_SIZE = 500 字），跟模型能吃多长原本毫无关系。碰上小窗口的模型
# （bge-small-zh 512、一些本地小模型 256 / 128），中文块会超：接口会 400（整个向量
# 那一路被迫关掉），或者更糟——静默截断，块的尾巴永远搜不到而且一声不响。
#
# 所以第一次要发向量之前先探一次，探测结果记在进程里（一个进程只探一遍）：
#   · 先拿一段约 _PROBE_TOP 个 token 的文本单发一条；
#   · 接口报 4xx = 吃不下，按阶梯往下找；
#   · 没报错，就再发一条三倍长的，比它自己报的 usage.prompt_tokens：
#     涨了 = 没截断；不涨（或者三倍那条直接报太长）= 它把输入掐住了，掐的那个数就是上限；
#   · 探不出来（网络不通、接口不报用量、返回看不懂）= 按「不限」，也就是回到老行为。
#
# 为什么要发两条来比：各家 tokenizer 的密度差得远（同样是中文，有的 1 字 1 token，
# 有的 1.5 字 1 token），拿我们自己的估算去跟它报的用量比一定会误判；拿它自己的两个
# 数互相比才是可靠的。
_PROBE_TOP = 900          # 第一档。现有块长（500 字，最坏全中文）估出来约 580 token，
                          # 这一档能完整过，就说明怎么切都不会超，直接收工
_PROBE_LADDER = (900, 512, 384, 256, 192, 128)
_PROBE_FLOOR = 64         # 探出来比这还小就没法用了（块会碎成渣），按不限处理
_PROBE_MARGIN = 0.9       # 比它报的用量再收一成，别卡着边界
_PROBE_STEPS = 3          # 上限夹在两档中间时，再二分几次（一次一条小请求）
_PROBE_TIMEOUT = 20       # 探测是阻塞建索引的，别用一个 60 秒的超时
# 只有这几个状态码才当「输入太长」。别把 4xx 一锅端：401 / 403 是 key 不对、
# 404 是地址写错、429 是限流，当成「太长」会让块长一路缩到最小还一声不响。
_TOO_LONG_CODES = (400, 413, 422)
_probed = {}              # {"模型@维度@地址": (上限, 说明)}，进程内只探一遍


class EmbedError(RuntimeError):
    """向量化失败。调用方接住它、把向量那一路关掉就行，别让整个索引建不起来。"""


class _TooManyItems(EmbedError):
    """一次塞的行数超过服务商上限。内部信号，embed_texts 会砍半重试，不往上报。"""


def enabled():
    """这一路到底用不用：后台那个开关关了就关；开着/没设过，还得模型、地址、key 配齐。"""
    return settings.embed_on()


def signature():
    """缓存用的指纹：只有「模型 + 维度」变了才需要重算向量。

    故意不含 key 和接口地址——换个 key 不该让几万个块的向量全部作废重花钱。
    """
    return f"{settings.embed_model()}@{EMBED_DIM}"


def describe():
    return f"{settings.embed_model()} @ {settings.embed_base_url()}"


def _headers():
    return {
        "Authorization": f"Bearer {settings.embed_key()}",
        "Content-Type": "application/json",
    }


def _probe_text(tokens):
    """造一段「我们自己估着约 tokens 个 token」的中文文本。

    全用中日韩字符，估算里 1 字就是 1 token，好算。对方 tokenizer 多密都不影响
    结论——探测比的是「它自己报的两个用量」，不是我们的估算。
    """
    unit = "内存取证与数据分析技术要点说明文档内容示例"
    tokens = max(1, int(tokens))
    return (unit * (tokens // len(unit) + 1))[:tokens]


def _ask(text):
    """单发一条（不是一批，这样 usage 才只属于这一条），返回 (状态, 它报的 token 数)。

    状态：ok（正常回来了）/ too_long（吃不下）/ no_usage（回来了但没报用量）/
    unknown（别的失败——不猜）。
    """
    url = settings.embed_base_url().rstrip("/") + "/embeddings"
    payload = {"model": settings.embed_model(), "input": [text]}
    try:
        resp = requests.post(url, headers=_headers(), json=payload, timeout=_PROBE_TIMEOUT)
    except Exception:
        return "unknown", 0
    if resp.status_code != 200:
        # 只有这几种才当「吃不下」。401 / 403 是 key 不对、404 是地址不对、429 是限流——
        # 那些跟长度无关，要是也当成「太长」，就会把块长一路缩到最小，还一路沉默地缩下去。
        return ("too_long", 0) if resp.status_code in _TOO_LONG_CODES else ("unknown", 0)
    try:
        body = resp.json() or {}
    except ValueError:
        return "unknown", 0
    used = (body.get("usage") or {}).get("prompt_tokens")
    if not isinstance(used, int) or used <= 0:
        return "no_usage", 0
    return "ok", used


def _probe_once(candidate):
    """探一档，返回 (状态, 上限)。状态：ok / too_long / truncated / unknown。"""
    status, first = _ask(_probe_text(candidate))
    if status == "too_long":
        return "too_long", 0
    if status == "unknown":
        return "unknown", 0
    if status == "no_usage":
        # 没报用量就只能确定「这一档它没报错」，比不了长短
        return "ok", 0
    status, second = _ask(_probe_text(candidate * 3))
    if status == "ok" and second > first * 1.5:
        return "ok", first          # 三倍长的用量跟着涨 = 没掐我们的输入
    if status == "too_long":
        # 三倍那条被挡了，说明上限夹在这一档和三倍之间。光拿 first 当上限太保守了
        # （实测有个模型真实上限 512，这么算会算成 352，块白切小三分之一），
        # 所以在两者之间再二分几次，找最大的「它收下的」那个数。
        best = first
        low, high = candidate, candidate * 3
        for _ in range(_PROBE_STEPS):
            if high - low <= max(24, low // 8):
                break
            middle = (low + high) // 2
            state, used = _ask(_probe_text(middle))
            if state == "ok":
                low, best = middle, max(best, used or 0)
            elif state == "too_long":
                high = middle
            else:
                break               # 限流 / 网络抖动就别继续猜了
        return "truncated", max(1, int(best * _PROBE_MARGIN))
    # 静默截断：它把输入掐到了 first 这个数
    return "truncated", max(1, int(first * _PROBE_MARGIN))


def _probe():
    """从大到小试，返回 (上限 token, 给人看的说明)。上限 0 = 不限。

    能一次探完就别多花请求：顶档过得去就直接收工——那是绝大多数情况（8K 窗口的模型
    到处都是，而我们的块最长才 580 token 左右）。
    """
    for candidate in _PROBE_LADDER:
        status, limit = _probe_once(candidate)
        if status == "unknown":
            return 0, "探不出来（接口没回应 / 返回看不懂），按不限处理"
        if status == "ok":
            if candidate == _PROBE_TOP:
                return 0, f"模型吃得下 {_PROBE_TOP} token 以上，现有块长不用收口"
            return candidate, f"模型上限约 {candidate} token，块长按它收口"
        if status == "truncated":
            if limit >= _PROBE_FLOOR:
                return limit, f"模型上限约 {limit} token（按它自己报的用量算的），块长按它收口"
            return 0, f"模型上限只有 {limit} token，小到没法切块了，按不限处理"
        # too_long：这一档吃不下，往下试
    # 连最小那一档都发不出去，多半不是长度问题（key / 模型名 / 地址不对），
    # 那就别乱缩块长，按不限处理
    return 0, f"连 {_PROBE_LADDER[-1]} token 都发不出去，看着不像长度问题（key / 模型名 / 地址？），按不限处理"


def max_input_tokens():
    """单条输入最多多少 token。0 = 不限（后台填了就用填的，没填自动探一次）。

    探测要走网络，所以结果记在进程里，一个进程只探一遍；索引重建不会重复探。
    """
    configured = settings.embed_max_tokens()
    if configured > 0:
        return configured
    key = f"{signature()}@{settings.embed_base_url()}"
    if key not in _probed:
        try:
            _probed[key] = _probe()
        except Exception as exc:      # 探测本身绝不能把建索引搞挂
            _probed[key] = (0, f"探测出错（{type(exc).__name__}），按不限处理")
    return _probed[key][0]


def probe_note():
    """上一次探测的结论，给后台显示用。还没探过就是空串。"""
    key = f"{signature()}@{settings.embed_base_url()}"
    entry = _probed.get(key)
    if entry:
        return entry[1]
    if settings.embed_max_tokens() > 0:
        return f"按后台填的 {settings.embed_max_tokens()} token 收口（没走自动探测）"
    return ""


def _post(texts):
    """发一批，失败重试几次。返回 list[list[float]]，顺序跟 texts 一致。"""
    url = settings.embed_base_url().rstrip("/") + "/embeddings"
    headers = _headers()
    # 不传 dimensions：有的服务商不认这个参数，传了反而 400。默认维度拿回来校验就行。
    payload = {"model": settings.embed_model(), "input": texts}
    want = EMBED_DIM
    last = ""

    for attempt in range(_RETRIES):
        try:
            resp = requests.post(url, headers=headers, json=payload, timeout=_TIMEOUT)
        except requests.RequestException as exc:
            last = f"{type(exc).__name__}: {exc}"  # 连不上 / 超时，退避重试还有救
        except Exception as exc:
            # 地址写错、key 里混进非 ASCII 字符这类，重试多少次都一样，直接报出去
            raise EmbedError(
                f"向量化请求发不出去（{describe()}）：{type(exc).__name__}: {exc}"
            ) from exc
        else:
            if resp.status_code == 200:
                try:
                    rows = (resp.json() or {}).get("data") or []
                except ValueError as exc:
                    raise EmbedError(f"返回的不是 JSON（{describe()}）：{exc}") from exc
                if len(rows) != len(texts):
                    raise EmbedError(
                        f"返回条数对不上：要 {len(texts)} 条，回来 {len(rows)} 条（{describe()}）"
                    )
                rows.sort(key=lambda item: item.get("index", 0))  # 别信它给的顺序
                vectors = [item["embedding"] for item in rows]
                got = len(vectors[0])
                if got != want:
                    raise EmbedError(
                        f"{settings.embed_model()} 返回的是 {got} 维，但 EMBED_DIM 配的是 {want} 维。"
                        f"把 EMBED_DIM 改成 {got}，或者删掉 .cache/ 重建索引"
                    )
                return vectors
            if resp.status_code == 400 and len(texts) > 1:
                # 多于一行的批次碰到 400，先当成「塞太多行了」——各家的上限不一样，
                # 报错措辞也五花八门，让上层砍半重发比猜文案稳。砍到只剩一行还 400，
                # 那就是这批内容本身有问题（比如单行 token 超长），如实报出去。
                raise _TooManyItems(f"HTTP 400: {resp.text[:200]}")
            last = f"HTTP {resp.status_code}: {resp.text[:200]}"
        if attempt + 1 < _RETRIES:  # 限流 / 网络抖动，退避一下再试
            time.sleep(1.5 * (attempt + 1))

    raise EmbedError(f"向量化失败（{describe()}）：{last}")


def embed_texts(texts):
    """把一批文本变成向量，顺序跟输入一致。

    接口嫌一次给的行太多就自动砍半重发，并把砍出来的安全值记下来给后面用。
    """
    global _batch
    texts = list(texts)
    if not texts:
        return []
    while True:
        batches = [texts[i:i + _batch] for i in range(0, len(texts), _batch)]
        try:
            if len(batches) == 1:
                return _post(batches[0])
            # map 按输入顺序返回结果，正好保证跟 batches 对齐
            with ThreadPoolExecutor(max_workers=min(_WORKERS, len(batches))) as pool:
                return [vector for chunk in pool.map(_post, batches) for vector in chunk]
        except _TooManyItems:
            # _post 只在多行的批次上抛这个，正常砍下去一定会收敛；留个兜底免得死循环
            if _batch <= 1:
                raise
            _batch = max(1, _batch // 2)


def embed_query(text):
    """检索时把问题也转向量。"""
    return embed_texts([text])[0]