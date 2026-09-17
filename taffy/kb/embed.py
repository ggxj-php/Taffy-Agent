"""向量化：调 OpenAI 兼容的 /embeddings 接口，把文本变成向量。

知识库检索的第二路。词匹配那套（kb/index.py 的 BM25）按字面词查，中文问题跟英文
教材在词表上零交集；向量把不同语言的同义内容映到相近位置，中文提问才搜得到英文书。

模型 / 接口地址 / key 都从 settings 里取，网页后台能改。三样没配齐就不启用，
检索自动退回纯词匹配，不会报错。
"""
import time
from concurrent.futures import ThreadPoolExecutor

import requests

from .. import settings
from ..config import EMBED_DIM

# 一次请求带多少条。百炼的文档写单次最多 20 行，留点余量；实测 25 也收。
_BATCH = 20
# 同时开几个请求。全库 8.5 万块要发 4000 多次请求，串行发太慢；4 路既快又不容易被限流。
_WORKERS = 4
_TIMEOUT = 60
_RETRIES = 3


class EmbedError(RuntimeError):
    """向量化失败。调用方接住它、把向量那一路关掉就行，别让整个索引建不起来。"""


def enabled():
    """模型 / 地址 / key 三样都配齐了才算启用。"""
    return bool(settings.embed_model() and settings.embed_base_url() and settings.embed_key())


def signature():
    """缓存用的指纹：只有「模型 + 维度」变了才需要重算向量。

    故意不含 key 和接口地址——换个 key 不该让几万个块的向量全部作废重花钱。
    """
    return f"{settings.embed_model()}@{EMBED_DIM}"


def describe():
    return f"{settings.embed_model()} @ {settings.embed_base_url()}"


def _post(texts):
    """发一批，失败重试几次。返回 list[list[float]]，顺序跟 texts 一致。"""
    url = settings.embed_base_url().rstrip("/") + "/embeddings"
    headers = {
        "Authorization": f"Bearer {settings.embed_key()}",
        "Content-Type": "application/json",
    }
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
            last = f"HTTP {resp.status_code}: {resp.text[:200]}"
        if attempt + 1 < _RETRIES:  # 限流 / 网络抖动，退避一下再试
            time.sleep(1.5 * (attempt + 1))

    raise EmbedError(f"向量化失败（{describe()}）：{last}")


def embed_texts(texts):
    """把一批文本变成向量，顺序跟输入一致。"""
    texts = list(texts)
    if not texts:
        return []
    batches = [texts[i:i + _BATCH] for i in range(0, len(texts), _BATCH)]
    if len(batches) == 1:
        return _post(batches[0])
    # map 按输入顺序返回结果，正好保证跟 batches 对齐
    with ThreadPoolExecutor(max_workers=min(_WORKERS, len(batches))) as pool:
        return [vector for chunk in pool.map(_post, batches) for vector in chunk]


def embed_query(text):
    """检索时把问题也转向量。"""
    return embed_texts([text])[0]