"""后台能改的运行配置：聊天模型、图片模型、API Key。

项目根目录下的 admin.json 当覆盖层，没配的项就回落到 config.py / .env 的默认值。
改完立刻生效不用重启——llm.py 每次请求都来问一次当前值。

这个文件里存着明文 key，所以已经写进 .gitignore 了，千万别提交。
"""
import json
import os
import threading

from .config import API_KEY, MODEL, PROJECT_ROOT, VISION_MODEL

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
        "api_key": str(raw.get("api_key") or ""),
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


def api_key():
    """当前生效的 key：后台配过就用后台的，否则用 .env 里的。"""
    return _load()["api_key"] or API_KEY


def key_source():
    """key 是从哪来的，后台拿来提示用：admin / env。"""
    return "admin" if _load()["api_key"] else "env"


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


def update_api_key(key):
    """换 key。下一条消息就会用新的。"""
    key = (key or "").strip()
    if not key:
        return
    with _lock:
        data = _load()
        data["api_key"] = key
        _write(data)
