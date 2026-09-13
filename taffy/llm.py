"""模型接入层：只负责发请求，不掺业务逻辑。"""
import threading

from openai import OpenAI

from . import settings
from .config import MAX_TOKENS

_clients = {}
_clients_lock = threading.Lock()


def _client(api_key, base_url):
    """按 (key, 接口地址) 建客户端。

    key 和地址都能在后台改，所以不能像以前那样在 import 时建一次就完事；
    这里缓存起来，换 key / 换地址之后的第一次请求就会自动用新的。

    聊天和图片可能是两家服务商（比如聊天 GLM、图片 DeepSeek），所以缓存键要带上
    地址——两个客户端各留着，不用每轮来回重建。
    """
    slot = (api_key, base_url)
    with _clients_lock:
        client = _clients.get(slot)
        if client is None:
            client = OpenAI(api_key=api_key, base_url=base_url)
            _clients[slot] = client
        return client


def stream_chat(messages: list, tools: list, model: str = "",
                api_key: str = "", base_url: str = ""):
    """流式发一次请求，边收边吐增量。

    依次产出 ("thinking", 片段) / ("content", 片段)，最后产出
    ("message", 拼好的 assistant 消息)，那条消息可以直接塞回 messages。

    model / api_key / base_url 留空就用后台配的聊天那套；带图的轮次由 core
    把图片那套的三个值传进来。
    """
    model = (model or "").strip() or settings.chat_model()
    settings.remember_model(model)
    key = (api_key or "").strip() or settings.chat_key()
    base = (base_url or "").strip() or settings.chat_base_url()

    stream = _client(key, base).chat.completions.create(
        model=model,
        messages=messages,
        tools=tools,
        max_tokens=MAX_TOKENS,
        stream=True,
    )

    text_parts = []
    calls = {}  # index -> {"id", "name", "arguments"}，流式下 tool_call 是分片下发的
    finish = None

    for chunk in stream:
        if not chunk.choices:
            continue
        choice = chunk.choices[0]
        if choice.finish_reason:
            finish = choice.finish_reason
        delta = choice.delta
        if delta is None:
            continue

        # 推理模型会先把思考过程放在 reasoning_content 里
        thought = getattr(delta, "reasoning_content", None)
        if thought:
            yield "thinking", thought

        if delta.content:
            text_parts.append(delta.content)
            yield "content", delta.content

        for piece in delta.tool_calls or []:
            slot = calls.setdefault(piece.index, {"id": "", "name": "", "arguments": ""})
            if piece.id:
                slot["id"] = piece.id
            if piece.function:
                if piece.function.name:
                    slot["name"] = piece.function.name
                if piece.function.arguments:
                    slot["arguments"] += piece.function.arguments

    text = "".join(text_parts)
    message = {"role": "assistant", "content": text or None}
    if calls:
        message["tool_calls"] = [
            {
                "id": slot["id"] or f"call_{index}",
                "type": "function",
                "function": {"name": slot["name"], "arguments": slot["arguments"]},
            }
            for index, slot in sorted(calls.items())
        ]
    if not message["content"] and not message.get("tool_calls"):
        # 一个字都没吐出来。stream 正常结束的情况下，多半是思考把 max_tokens 吃光了；
        # 要是 finish 也不是 length，那就是流被中途掐断的（网络/代理），报个清楚的错，
        # 让 core 去处理——绝不能把 content 为 None 的消息塞进历史，那会让会话之后永远 400。
        if finish == "length":
            raise RuntimeError(
                "模型光思考没吐正文就结束了（输出被 max_tokens 截断，可以在 config.py 里调大 MAX_TOKENS）"
            )
        raise RuntimeError(f"模型没返回任何内容（finish_reason={finish}）")

    yield "message", message
