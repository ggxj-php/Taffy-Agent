"""后台管理：登录、改模型、改 Key、改知识库的向量模型。挂在 /admin 和 /api/admin/* 底下。

口令是按天变的：md5(.env 里的 ADMIN_PASSWORD_PREFIX + 当天日期 YYMMDD)，日期按
UTC+8 算——服务器时钟是 UTC 也不会差一天。口令只在内存里比对，不落盘、不写日志。

**这里刻意不留任何默认前缀**：前缀是口令里唯一的秘密，写进代码就等于公开了。
没配的话登录直接拒绝，并提示去 .env 里配。

登录成功发一个随机 token 的 cookie，12 小时有效；进程重启就全失效，得重新登。
"""
import hashlib
import hmac
import os
import secrets
import threading
import time
from datetime import datetime, timedelta, timezone

from fastapi import APIRouter, HTTPException, Request, Response
from fastapi.responses import FileResponse
from pydantic import BaseModel

from .. import settings
from ..config import ADMIN_PASSWORD_PREFIX, EMBED_DIM
from ..kb import stats as kb_stats

router = APIRouter()

STATIC_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "static")

COOKIE_NAME = "taffy_admin"
TOKEN_TTL = 12 * 3600
_TOKENS = {}
_TOKENS_LOCK = threading.Lock()


def _digest(text):
    return hashlib.md5(text.encode("utf-8")).hexdigest()


def _beijing_now():
    """按北京时间取「当前」。服务器跑在 UTC 上也不会把日期算错一天。"""
    return datetime.now(timezone.utc) + timedelta(hours=8)


def expected_password(day=None):
    """当天口令的 md5。动态的就是日期那一段；前缀没配的话这个值没意义，
    登录那条路会先拦下来。"""
    return _digest(ADMIN_PASSWORD_PREFIX + (day or _beijing_now()).strftime("%y%m%d"))


def check_password(password):
    """比对 md5，别拿明文字符串直接比。没配前缀一律不放行。"""
    if not ADMIN_PASSWORD_PREFIX:
        return False
    if not isinstance(password, str) or not password:
        return False
    return hmac.compare_digest(_digest(password), expected_password())


def _issue_token():
    token = secrets.token_urlsafe(32)
    now = time.time()
    with _TOKENS_LOCK:
        for old, expire in list(_TOKENS.items()):
            if expire < now:
                del _TOKENS[old]
        _TOKENS[token] = now + TOKEN_TTL
    return token


def _logged_in(request):
    token = request.cookies.get(COOKIE_NAME)
    if not token:
        return False
    with _TOKENS_LOCK:
        expire = _TOKENS.get(token)
    return bool(expire and expire > time.time())


def _require(request):
    if not _logged_in(request):
        raise HTTPException(status_code=401, detail="先登录喵")


def _state():
    return {
        "model": settings.chat_model(),
        "vision_model": settings.vision_model(),
        "model_history": settings.model_history(),
        # key 本身不回给前端，只说它是从哪来的：admin（后台配的）/ env（.env 里的）。
        # 接口地址不是秘密，直接把当前生效的值给出去，页面拿它当占位提示。
        "chat_key_source": settings.key_source(vision=False),
        "vision_key_source": settings.key_source(vision=True),
        "chat_base_url": settings.chat_base_url(),
        "vision_base_url": settings.vision_base_url(),
        "chat_base_source": settings.base_source(vision=False),
        "vision_base_source": settings.base_source(vision=True),
        # 知识库向量检索那一路（跟聊天 / 图片两套没关系，是检索用的）
        "embed_model": settings.embed_model(),
        "embed_base_url": settings.embed_base_url(),
        "embed_key_source": settings.embed_key_source(),
        "embed_base_source": settings.embed_base_source(),
        "embed_dim": EMBED_DIM,
        "kb": kb_stats(),
    }


@router.get("/admin")
def admin_page():
    return FileResponse(os.path.join(STATIC_DIR, "admin.html"))


class LoginRequest(BaseModel):
    password: str = ""


@router.post("/api/admin/login")
def login(req: LoginRequest, response: Response):
    if not ADMIN_PASSWORD_PREFIX:
        raise HTTPException(
            status_code=503,
            detail="后台口令还没配喵：在 .env 里加一行 ADMIN_PASSWORD_PREFIX=你自己定的一串，再重启服务",
        )
    if not check_password(req.password):
        raise HTTPException(status_code=401, detail="口令不对喵")
    response.set_cookie(
        COOKIE_NAME,
        _issue_token(),
        max_age=TOKEN_TTL,
        httponly=True,   # 前端 JS 读不到，少一个被偷的口子
        samesite="lax",
    )
    return {"ok": True}


@router.post("/api/admin/logout")
def logout(request: Request, response: Response):
    token = request.cookies.get(COOKIE_NAME)
    with _TOKENS_LOCK:
        _TOKENS.pop(token, None)
    response.delete_cookie(COOKIE_NAME)
    return {"ok": True}


@router.get("/api/admin/state")
def state(request: Request):
    _require(request)
    return _state()


class ModelsRequest(BaseModel):
    model: str = ""
    vision_model: str = ""


@router.post("/api/admin/models")
def save_models(req: ModelsRequest, request: Request):
    _require(request)
    model = req.model.strip()
    vision = req.vision_model.strip()
    if not model or not vision:
        raise HTTPException(status_code=400, detail="两个模型名都得填喵")
    settings.update_models(model, vision)
    return _state()


class KeysRequest(BaseModel):
    # 四个都留空表示「这项不改」——只想换聊天 key 时不用把图片那套重填一遍
    chat_key: str = ""
    vision_key: str = ""
    chat_base_url: str = ""
    vision_base_url: str = ""


def _check_base(name, value):
    value = value.strip()
    if value and not value.startswith(("http://", "https://")):
        raise HTTPException(status_code=400, detail=f"{name}的接口地址要以 http:// 或 https:// 开头喵")
    return value


@router.post("/api/admin/keys")
def save_keys(req: KeysRequest, request: Request):
    _require(request)
    chat_base = _check_base("聊天", req.chat_base_url)
    vision_base = _check_base("图片", req.vision_base_url)
    chat_key = req.chat_key.strip()
    vision_key = req.vision_key.strip()
    if not (chat_key or vision_key or chat_base or vision_base):
        raise HTTPException(status_code=400, detail="一个都没填，那就先不动它喵")
    settings.update_keys(chat_key, vision_key, chat_base, vision_base)
    return _state()


class EmbedRequest(BaseModel):
    embed_model: str = ""
    embed_base_url: str = ""
    embed_key: str = ""


@router.post("/api/admin/embed")
def save_embed(req: EmbedRequest, request: Request):
    _require(request)
    base = _check_base("向量模型", req.embed_base_url)
    model = req.embed_model.strip()
    key = req.embed_key.strip()
    if not (model or base or key):
        raise HTTPException(status_code=400, detail="一个都没填，那就先不动它喵")
    settings.update_embed(model, base, key)
    return _state()
