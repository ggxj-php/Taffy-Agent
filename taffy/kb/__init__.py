"""知识库：对外是 search() / warmup() / stats()，索引在第一次用到时懒加载。

索引是进程内单例，只建一次。运行中往 knowledge/ 里加了文件不会自动生效，
重启一下就好。

检索走几路（原查询词匹配 + 英文检索词 + 向量），细节见 index.py。索引在后台线程里建：
建好之前 search() 拿到的是个半成品；索引本身是同步就绪的，向量那一路算好了下一问就自动用上。
"""
import threading

from ..config import KB_TOP_K
from .index import KnowledgeBase

_kb = None
_lock = threading.Lock()
# 后台页面拿它显示索引进度：还在建吗、向量算了多少、有没有出错
_stats = {"building": False, "chunks": 0, "vectors": 0, "error": ""}


def _get():
    global _kb
    if _kb is None:
        _kb = KnowledgeBase()
        _kb.build()
    return _kb


def warmup():
    """提前把索引建好，别让第一个提问卡在建索引上。"""
    with _lock:
        _stats["building"] = True
    try:
        kb = _get()
        with _lock:
            _stats["chunks"] = len(kb.chunks)
            _stats["vectors"] = kb.vector_count()
            _stats["error"] = kb.vector_error
    except Exception as exc:
        with _lock:
            _stats["error"] = f"{type(exc).__name__}: {exc}"
        raise
    finally:
        with _lock:
            _stats["building"] = False


def stats():
    """索引状态，给网页后台看的。"""
    with _lock:
        return dict(_stats)


def search(query, top_k=KB_TOP_K):
    """检索知识库，返回拼好的原文片段（带出处），供模型直接阅读。"""
    kb = _get()

    if not kb.chunks:
        return (
            "知识库是空的。把文档放进项目根目录的 knowledge/ 文件夹再试，"
            "支持 pdf / docx / html / md / txt。"
        )

    hits = kb.search(query, top_k)
    if not hits:
        return f"知识库里没找到和「{query}」相关的内容。"

    # 不打分数：各路融合后的分数是个很小的名次分，写出来反而会让人误判相关性
    blocks = []
    for _score, chunk in hits:
        page = f" 第 {chunk['page']} 页" if chunk.get("page") else ""
        blocks.append(f"【{chunk['source']}{page}】\n{chunk['text']}")
    return "\n\n".join(blocks)