"""会话存档：把一段聊天的上下文存成 txt，放在项目根目录的 sessions/ 下。

**存文件，不存内存**——服务器只有 2G，历史全堆在进程里迟早 OOM；存成 txt 还能直接
拿编辑器打开看。

文件名就是主人自己起的 uuid，所以：
· uuid 有格式要求（字母数字加 . _ - ，3~64 位，不能以点开头）；
· 保存前先查重，重名直接拒绝，绝不覆盖已经存过的那份（重了就换个名字）。
"""
import os
import re
import time

from ..config import SESSIONS_DIR

# 只收这种 uuid：字母开头、只含字母数字和 . _ -，3~64 位。别的一律拒绝——
# 它会长成磁盘上的文件名，宽一点就是路径穿越的口子。
_UUID_OK = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{1,63}$")

MAX_READ_CHARS = 400 * 1024   # 单个存档最多读这么多字符给后台看，别拿大文件把内存顶了

os.makedirs(SESSIONS_DIR, exist_ok=True)


def check_uuid(value):
    """校验 uuid，返回规整后的值；不合法抛 ValueError。"""
    value = (value or "").strip()
    if not value:
        raise ValueError("会话 uuid 不能空着喵")
    if ".." in value or not _UUID_OK.match(value):
        raise ValueError("uuid 只能用字母、数字和 . _ -（3~64 位，字母或数字开头）喵")
    return value


def path_of(value):
    return os.path.join(SESSIONS_DIR, check_uuid(value) + ".txt")


def exists(value):
    try:
        return os.path.isfile(path_of(value))
    except ValueError:
        return False


def _content_of(message):
    """把一条消息的 content 拍成纯文本。带图那轮 content 是个列表，这里只留一句说明。"""
    content = message.get("content")
    if isinstance(content, list):
        texts = [part.get("text", "") for part in content
                 if isinstance(part, dict) and part.get("type") == "text"]
        has_image = any(isinstance(part, dict) and part.get("type") == "image_url"
                        for part in content)
        text = "\n".join(t for t in texts if t)
        return (text + "\n[图片]" if has_image else text).strip()
    return (content or "").strip()


def render(messages, uuid):
    """把对话历史拍成给人看的 txt。系统提示词不写进去（那是人设，不是聊天内容）。"""
    stamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    lines = [
        "# 永雏塔菲 · 会话存档",
        f"# 会话 uuid：{uuid}",
        f"# 保存时间：{stamp}（服务器本地时间）",
        f"# 共 {len(messages)} 条记录（含工具调用与结果）",
        "",
    ]
    index = 0
    for message in messages:
        role = message.get("role")
        if role == "system":
            continue          # 人设提示词不进去，存档只留对话本身
        index += 1
        if role == "user":
            who = "你"
        elif role == "assistant":
            who = "塔菲"
        else:
            who = "工具结果"
        body = _content_of(message)
        calls = message.get("tool_calls") or []
        if calls:
            names = [c.get("function", {}).get("name", "?") for c in calls]
            note = "（调用了工具：" + "、".join(names) + "）"
            body = (body + "\n" + note).strip() if body else note
        if not body:
            body = "（这一条没有正文）"
        lines += ["-" * 60, f"[{index}] {who}", "", body, ""]
    return "\n".join(lines)


def save(uuid, messages):
    """存一份存档。重名抛 FileExistsError，让调用方给主人一句人话。"""
    uuid = check_uuid(uuid)
    target = path_of(uuid)
    if os.path.exists(target):
        raise FileExistsError(uuid)
    text = render(messages, uuid)
    # 先写临时文件再改名：中途出错也不会留下半截存档
    tmp = target + ".part"
    with open(tmp, "w", encoding="utf-8") as fp:
        fp.write(text)
    os.replace(tmp, target)
    return {
        "uuid": uuid,
        "file": os.path.basename(target),
        "messages": len(messages),
        "bytes": len(text.encode("utf-8")),
    }


def _preview(text):
    """预览：第一句「你」说的话，截一小段，列表里能认出是哪个会话就行。"""
    lines = text.splitlines()
    for i, line in enumerate(lines):
        if line.startswith("[") and line.endswith("] 你"):
            for follow in lines[i + 1:]:
                follow = follow.strip()
                if follow and not follow.startswith("-"):
                    return follow[:60]
            break
    return "（没有用户发言）"


def list_all():
    """列出所有存档（新存的在前）。只读每个文件开头一点，不整个读进来。"""
    items = []
    try:
        names = os.listdir(SESSIONS_DIR)
    except OSError:
        return items
    for name in names:
        if not name.endswith(".txt"):
            continue
        full = os.path.join(SESSIONS_DIR, name)
        if not os.path.isfile(full):
            continue
        try:
            stat = os.stat(full)
            with open(full, "r", encoding="utf-8", errors="replace") as fp:
                head = fp.read(4096)
        except OSError:
            continue
        items.append({
            "uuid": name[:-4],
            "file": name,
            "size": stat.st_size,
            "mtime": int(stat.st_mtime),
            "preview": _preview(head),
        })
    items.sort(key=lambda it: it["mtime"], reverse=True)
    return items


def read(uuid, limit=MAX_READ_CHARS):
    """读一份存档的正文。超大文件截断，返回 (文本, 是否被截断)。"""
    full = path_of(uuid)
    if not os.path.isfile(full):
        raise FileNotFoundError(uuid)
    with open(full, "r", encoding="utf-8", errors="replace") as fp:
        text = fp.read(limit + 1)
    if len(text) > limit:
        return text[:limit], True
    return text, False


def remove(uuid):
    full = path_of(uuid)
    if not os.path.isfile(full):
        raise FileNotFoundError(uuid)
    os.remove(full)
    return os.path.basename(full)