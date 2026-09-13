"""后台管理：登录、改模型、改 Key。挂在 /admin 和 /api/admin/* 底下。

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
from ..config import ADMIN_PASSWORD_PREFIX

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
        # key 本身不回给前端，只说它是从哪来的：admin（后台配的）/ env（.env 里的）
        "key_source": settings.key_source(),
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


class KeyRequest(BaseModel):
    api_key: str = ""


@router.post("/api/admin/key")
def save_key(req: KeyRequest, request: Request):
    _require(request)
    key = req.api_key.strip()
    if not key:
        raise HTTPException(status_code=400, detail="key 不能留空喵")
    settings.update_api_key(key)
    return _state()
