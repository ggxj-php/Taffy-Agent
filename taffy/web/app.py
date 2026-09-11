"""网页后端：把 TaffyAgent 的事件流用 SSE 吐给浏览器。

会话隔离靠 session_id：每个 id 对应一个独立的 TaffyAgent 实例，历史各自独立，
前端开新会话就是换一个 id。TaffyAgent 构造时第一条永远是 SYSTEM_PROMPT，
所以就算前端乱传也不会把人设弄丢。
"""
import json
import os
import threading
import uuid
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.responses import FileResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from ..core import TaffyAgent
from ..kb import warmup

STATIC_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "static")


@asynccontextmanager
async def lifespan(_app):
    # 后台先把知识库索引建好（约几秒），第一个提问就不用干等
    threading.Thread(target=warmup, daemon=True).start()
    yield


app = FastAPI(title="Taffy Agent", lifespan=lifespan)
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

# session_id -> {"agent": TaffyAgent, "lock": Lock}
_sessions = {}
_sessions_lock = threading.Lock()


class ChatRequest(BaseModel):
    session_id: str
    message: str = ""
    # 可选的内联图片（data:image/...;base64,...）。不落盘，这一轮跑完就丢。
    image: str | None = None


def _session(session_id):
    """按 id 取会话，没有就现场开一个。"""
    with _sessions_lock:
        entry = _sessions.get(session_id)
        if entry is None:
            entry = {"agent": TaffyAgent(), "lock": threading.Lock()}
            _sessions[session_id] = entry
        return entry


@app.get("/")
def index():
    return FileResponse(os.path.join(STATIC_DIR, "index.html"))


@app.post("/api/session")
def new_session():
    """开一个新会话，返回它的 id。"""
    session_id = uuid.uuid4().hex
    _session(session_id)
    return {"session_id": session_id}


@app.post("/api/chat")
def chat(req: ChatRequest):
    """收一条消息，把 agent 的事件流原样转成 SSE 返回。"""
    entry = _session(req.session_id)

    def events():
        # 同一个会话串行处理，避免两条消息交叉写乱历史
        with entry["lock"]:
            for event in entry["agent"].ask_stream(req.message, req.image):
                yield f"data: {json.dumps(event, ensure_ascii=False)}\n\n"
        yield "data: [DONE]\n\n"

    return StreamingResponse(
        events(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no",
        },
    )
