"""知识库：对外是 search() 和 warmup()，索引在第一次用到时懒加载。

索引是进程内单例，只建一次。运行中往 knowledge/ 里加了文件不会自动生效，
重启一下就好。
"""
from ..config import KB_TOP_K
from .index import KnowledgeBase

_kb = None


def _get():
    global _kb
    if _kb is None:
        _kb = KnowledgeBase()
        _kb.build()
    return _kb


def warmup():
    """提前把索引建好，别让第一个提问卡在建索引上。"""
    _get()


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

    blocks = []
    for score, chunk in hits:
        page = f" 第 {chunk['page']} 页" if chunk.get("page") else ""
        blocks.append(f"【{chunk['source']}{page}】(score {score:.2f})\n{chunk['text']}")
    return "\n\n".join(blocks)
