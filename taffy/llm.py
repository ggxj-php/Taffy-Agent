"""模型接入层：只负责发请求，不掺业务逻辑。"""
from openai import OpenAI

from .config import API_KEY, BASE_URL, MODEL

client = OpenAI(api_key=API_KEY, base_url=BASE_URL)


def stream_chat(messages: list, tools: list):
    """流式发一次请求，边收边吐增量。

    依次产出 ("thinking", 片段) / ("content", 片段)，最后产出
    ("message", 拼好的 assistant 消息)，那条消息可以直接塞回 messages。
    """
    stream = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        tools=tools,
        stream=True,
    )

    text_parts = []
    calls = {}  # index -> {"id", "name", "arguments"}，流式下 tool_call 是分片下发的

    for chunk in stream:
        if not chunk.choices:
            continue
        delta = chunk.choices[0].delta
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
    yield "message", message
