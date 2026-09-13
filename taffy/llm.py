"""模型接入层：只负责发请求，不掺业务逻辑。"""
from openai import OpenAI

from .config import API_KEY, BASE_URL, MAX_TOKENS, MODEL

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
        max_tokens=MAX_TOKENS,
        stream=True,
    )

    text_parts = []
    calls = {}  # index -> {"id", "name", "arguments"}，流式下 tool_call 是分片下发的
    finish = None  # 结束原因，"length" 表示被 max_tokens 截断

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
    elif not text:
        # 既没有正文、也没有工具调用。这种消息发给 API 会被判非法（400：
        # content or tool_calls must be set），一旦写进历史，整个会话之后每次都 400。
        # 所以这里直接报错，让上层走 error 分支，不把它记进对话历史。
        # 最常见的成因：思考把 max_tokens 吃光了，正文没轮到输出。
        raise RuntimeError(
            "模型光思考没吐正文就结束了（%s），这一轮作废，直接再问一次就好"
            % ("输出被 max_tokens 截断，可以在 config.py 里调大 MAX_TOKENS" if finish == "length"
               else "原因不明")
        )
    yield "message", message
