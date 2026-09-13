"""后台能改的运行配置：模型、接口地址、API Key。

项目根目录下的 admin.json 当覆盖层，没配的项就回落到 config.py / .env 的默认值。
改完立刻生效不用重启——llm.py 每次请求都来问一次当前值。

聊天和图片是两套独立的连接：可以聊天用 GLM、发图用 DeepSeek，模型名、key、
接口地址各配各的，互不影响；某一套没配就回落到 config.py / .env 给它那套的默认值
（老版本只有一个 api_key，读进来当成聊天那套）。

这个文件里存着明文 key，所以已经写进 .gitignore 了，千万别提交。
"""
import json
import os
import threading

from .config import (
    API_KEY,
    BASE_URL,
    MODEL,
    PROJECT_ROOT,
    VISION_API_KEY,
    VISION_BASE_URL,
    VISION_MODEL,
)

SETTINGS_PATH = os.path.join(PROJECT_ROOT, "admin.json")

# 历史模型列表最多留这么多条，免得越攒越长
HISTORY_LIMIT = 30

_lock = threading.Lock()
_cache = None


def _load():
    """读文件。文件不存在 / 坏了就当没配过，绝不让后台把服务搞挂。"""
    global _cache
    if _cache is not None:
        return _cache
    raw = {}
    try:
        with open(SETTINGS_PATH, "r", encoding="utf-8") as fp:
            loaded = json.load(fp)
        if isinstance(loaded, dict):
            raw = loaded
    except (OSError, ValueError):
        raw = {}

    history = raw.get("model_history")
    _cache = {
        # 老版本只存了一个 api_key，当成聊天那套读
        "chat_key": str(raw.get("chat_key") or raw.get("api_key") or ""),
        "vision_key": str(raw.get("vision_key") or ""),
        "chat_base": str(raw.get("chat_base") or ""),
        "vision_base": str(raw.get("vision_base") or ""),
        "model": str(raw.get("model") or ""),
        "vision_model": str(raw.get("vision_model") or ""),
        "model_history": [m for m in history if isinstance(m, str)] if isinstance(history, list) else [],
    }
    return _cache


def _write(data):
    """先写临时文件再替换，避免写一半断电留下半截 JSON。"""
    tmp = SETTINGS_PATH + ".tmp"
    with open(tmp, "w", encoding="utf-8") as fp:
        json.dump(data, fp, ensure_ascii=False, indent=2)
    os.replace(tmp, SETTINGS_PATH)
    try:
        os.chmod(SETTINGS_PATH, 0o600)  # 里面有 key，别让别的用户读到
    except OSError:
        pass  # Windows 上不认这个权限位，忽略


# ---------- 模型 ----------

def chat_model():
    """平时聊天用的模型。"""
    return _load()["model"] or MODEL


def vision_model():
    """发图片时用的模型。"""
    return _load()["vision_model"] or VISION_MODEL


def model_for(vision):
    """有图片就走图片模型，纯文字走聊天模型，两个都在后台单独配。"""
    return vision_model() if vision else chat_model()


def model_history():
    """用过的模型，新的在前，后台拿它当候选列表。"""
    return list(_load()["model_history"])


def remember_model(name):
    """记下这次真正用到的模型。已经记过就不重复写盘。"""
    name = (name or "").strip()
    if not name:
        return
    with _lock:
        data = _load()
        if name in data["model_history"]:
            return
        data["model_history"].insert(0, name)
        del data["model_history"][HISTORY_LIMIT:]
        _write(data)


def update_models(model, vision):
    """存两个模型名，顺手记进历史列表。"""
    model = (model or "").strip()
    vision = (vision or "").strip()
    with _lock:
        data = _load()
        data["model"] = model
        data["vision_model"] = vision
        for name in (model, vision):
            if name and name not in data["model_history"]:
                data["model_history"].insert(0, name)
        del data["model_history"][HISTORY_LIMIT:]
        _write(data)


# ---------- Key ----------

def chat_key():
    """聊天那套的 key：后台配过就用后台的，否则用 .env 里的。"""
    return _load()["chat_key"] or API_KEY


def vision_key():
    """图片那套的 key。没单独配就用 .env / config.py 里给图片那套配的默认值。"""
    return _load()["vision_key"] or VISION_API_KEY


def key_for(vision=False):
    return vision_key() if vision else chat_key()


def key_source(vision=False):
    """key 是哪来的，后台拿来提示用：admin（后台配的）/ env（.env 里的）。"""
    return "admin" if _load()["vision_key" if vision else "chat_key"] else "env"


# ---------- 接口地址 ----------

def chat_base_url():
    """聊天那套的接口地址。"""
    return _load()["chat_base"] or BASE_URL


def vision_base_url():
    """图片那套的接口地址。没单独配就用 config.py 给图片那套配的默认值。"""
    return _load()["vision_base"] or VISION_BASE_URL


def base_url_for(vision=False):
    return vision_base_url() if vision else chat_base_url()


def base_source(vision=False):
    """接口地址是哪来的，后台拿来提示用：admin（后台配的）/ default（config.py 里的）。"""
    return "admin" if _load()["vision_base" if vision else "chat_base"] else "default"


def update_keys(chat_key_new, vision_key_new, chat_base, vision_base):
    """换 key / 换接口地址。

    每一项留空就表示「这项不改」——这样只想换聊天 key 的时候，不用把图片那套
    重新填一遍。
    """
    with _lock:
        data = _load()
        if chat_key_new:
            data["chat_key"] = chat_key_new
        if vision_key_new:
            data["vision_key"] = vision_key_new
        if chat_base:
            data["chat_base"] = chat_base
        if vision_base:
            data["vision_base"] = vision_base
        _write(data)
