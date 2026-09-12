"""文本与数据解析小工具：正则调试、文本差异、JSON 处理。

写代码、对配置、比日志的时候天天要用，纯标准库、纯内存计算，不联网、不起子进程，
所有输入都是直接传字符串，不用先在 workspace 里落一个文件。
"""
import difflib
import itertools
import json
import re

MAX_TEXT = 100000        # 单个入参最多这么长
MAX_PATTERN = 500
MAX_MATCHES = 200
MAX_OUTPUT = 6000        # 结果输出最多这么多字符
MAX_LINES = 4000

_FLAGS = {"i": re.I, "m": re.M, "s": re.S, "x": re.X, "a": re.A, "u": re.U}

SPECS = [
    {
        "type": "function",
        "function": {
            "name": "regex_test",
            "description": (
                "正则表达式测试：给一个正则和一段文本，列出每一处匹配的位置、内容和各分组"
                "（命名分组会标出组名）；再给 replace 就顺带做替换（支持 \\1、\\g<name> 反向引用）。"
                "flags 可以传 i / m / s / x 的组合。写正则、抠日志、验规则的时候用它。"
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "pattern": {"type": "string", "description": "正则表达式，如 (?P<y>\\d{4})-(\\d{2})"},
                    "text": {"type": "string", "description": "要匹配的文本"},
                    "flags": {"type": "string", "description": "可选。i 忽略大小写 / m 多行 / s 让 . 匹配换行 / x 宽松格式，可组合，如 \"im\""},
                    "replace": {"type": "string", "description": "可选。给了就返回替换后的文本"},
                    "max_matches": {"type": "integer", "description": "最多列几处匹配，默认 200"},
                },
                "required": ["pattern", "text"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "diff_text",
            "description": "对比两段文本 / 代码的差异，输出 unified diff 并统计新增 / 删除了几行。对日志、对配置、看两版代码改了什么用它。",
            "parameters": {
                "type": "object",
                "properties": {
                    "a": {"type": "string", "description": "旧的那段文本（原来的 / 左边的）"},
                    "b": {"type": "string", "description": "新的那段文本（改后的 / 右边的）"},
                    "context": {"type": "integer", "description": "每处差异上下各显示几行，默认 3"},
                },
                "required": ["a", "b"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "json_tool",
            "description": (
                "JSON 处理：op=format 缩进美化（默认，中文不转义成 \\uXXXX）、op=minify 压成一行、"
                "op=get 按路径取值（如 data.items[0].name）、op=validate 只校验。语法错会指出第几行第几列并画出来。"
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "data": {"type": "string", "description": "JSON 文本"},
                    "op": {"type": "string", "enum": ["format", "minify", "get", "validate"], "description": "默认 format"},
                    "path": {"type": "string", "description": "op=get 时要取哪一块，如 items[2].name"},
                    "indent": {"type": "integer", "description": "op=format 缩进几个空格，默认 2"},
                },
                "required": ["data"],
            },
        },
    },
]


# ---------------- 公共小工具 ----------------

def _clip(text: str) -> str:
    if len(text) > MAX_OUTPUT:
        return text[:MAX_OUTPUT] + "\n…（内容太长，先给到这儿）"
    return text


def _visible(text: str, limit: int = 200) -> str:
    """把换行 / 制表符显示成转义写法，免得结果里一片乱。"""
    shown = (text.replace("\\", "\\\\").replace("\n", "\\n")
                 .replace("\r", "\\r").replace("\t", "\\t"))
    if len(shown) > limit:
        shown = shown[:limit] + "…"
    return shown


# ---------------- regex_test ----------------

def _risky_pattern(pattern: str) -> bool:
    """抓 (a+)+ / (.*)* 这种嵌套量词。re 模块没法设超时，只能先拦下来，
    否则一个恶意 / 写错的正则能把整个服务卡死。"""
    spans = []
    stack = []
    escaped = in_class = False
    for index, ch in enumerate(pattern):
        if escaped:
            escaped = False
        elif ch == "\\":
            escaped = True
        elif in_class:
            in_class = ch != "]"
        elif ch == "[":
            in_class = True
        elif ch == "(":
            stack.append(index)
        elif ch == ")" and stack:
            spans.append((stack.pop(), index))
    unbounded = re.compile(r"[*+]|\{\d+,\}")
    followed = re.compile(r"^[*+]|^\{\d+,\}")
    for start, end in spans:
        if unbounded.search(pattern[start + 1:end]) and followed.match(pattern[end + 1:]):
            return True
    return False


def regex_test(pattern: str = "", text: str = "", flags: str = "", replace: str = "",
               max_matches: int = MAX_MATCHES) -> str:
    """跑一遍正则，把匹配 / 分组 / 替换结果列出来。"""
    if not pattern:
        return "得先给我一个正则表达式呀喵"
    if len(pattern) > MAX_PATTERN:
        return f"正则太长了（{len(pattern)} 字符，最多 {MAX_PATTERN}）"
    if len(text) > MAX_TEXT:
        return f"文本太长了（{len(text)} 字符，最多 {MAX_TEXT}）"
    try:
        limit = max(1, min(int(max_matches), MAX_MATCHES))
    except (TypeError, ValueError):
        limit = MAX_MATCHES

    flag_value = 0
    for ch in (flags or "").strip():
        if ch not in _FLAGS:
            return f"不认识的 flags：{ch}（能用的只有 i m s x a u）"
        flag_value |= _FLAGS[ch]
    try:
        compiled = re.compile(pattern, flag_value)
    except re.error as e:
        return f"这个正则写错了：{e}"
    if _risky_pattern(pattern):
        return ("这个正则里有嵌套量词（像 (a+)+ 这种写法），跑起来可能会指数级回溯卡死，"
                "先改写成不会灾难性回溯的版本再来喵")

    try:
        matches = list(itertools.islice(compiled.finditer(text), limit))
        lines = [
            f"正则：{pattern}",
            f"文本：{len(text)} 字符" + (f"，flags={flags.strip()}" if flags.strip() else ""),
        ]
        if not matches:
            lines.append("一处都没匹配上")
        else:
            if len(matches) == limit:
                lines.append(f"匹配到至少 {len(matches)} 处（只列前 {limit} 处）：")
            else:
                lines.append(f"匹配到 {len(matches)} 处：")
            names = {index: name for name, index in compiled.groupindex.items()}
            for order, match in enumerate(matches, 1):
                start, end = match.span()
                lines.append(f"{order}) [{start}..{end}] {_visible(match.group(0))}")
                for index, value in enumerate(match.groups(), 1):
                    label = f"组 {index}" + (f" ({names[index]})" if index in names else "")
                    lines.append(f"   {label} = " + ("（空，没匹配到）" if value is None else _visible(value)))
        if replace:
            replaced = compiled.sub(replace, text)
            lines.append(f"替换结果（{len(text)} → {len(replaced)} 字符）：")
            lines.append(replaced if replaced else "（空字符串）")
    except re.error as e:
        return f"匹配的时候出错了：{e}"
    return _clip("\n".join(lines))


# ---------------- diff_text ----------------

def diff_text(a: str = "", b: str = "", context: int = 3) -> str:
    """两段文本的 unified diff。"""
    if not a and not b:
        return "两段都是空的，没法比喵"
    if len(a) > MAX_TEXT or len(b) > MAX_TEXT:
        return f"两边都要在 {MAX_TEXT} 字符以内"
    try:
        around = max(0, min(int(context), 20))
    except (TypeError, ValueError):
        around = 3

    lines_a, lines_b = a.splitlines(), b.splitlines()
    diff = list(difflib.unified_diff(lines_a, lines_b, fromfile="旧", tofile="新",
                                     n=around, lineterm=""))
    if not diff:
        same = "两边一模一样，没有差异"
        if a != b:      # 行内内容一样，差的只是行尾换行之类
            same += "（只有末尾换行 / 行尾这些细节不一样）"
        return same
    if len(diff) > MAX_LINES:
        diff = diff[:MAX_LINES]
        diff.append(f"…（差异太多，只列前 {MAX_LINES} 行）")
    added = sum(1 for line in diff if line.startswith("+") and not line.startswith("+++"))
    removed = sum(1 for line in diff if line.startswith("-") and not line.startswith("---"))
    header = (f"{len(lines_a)} 行 → {len(lines_b)} 行；新增 {added} 行，删除 {removed} 行"
              f"（上下文 {around} 行）")
    note = "（- 是旧的那边，+ 是新的那边）"
    return _clip("\n".join([header, note, "", *diff]))


# ---------------- json_tool ----------------

def _json_error(data: str, exc: json.JSONDecodeError) -> str:
    lines = [f"JSON 不合法：{exc.msg}（第 {exc.lineno} 行第 {exc.colno} 列）"]
    source = data.splitlines()
    if 1 <= exc.lineno <= len(source):
        bad = source[exc.lineno - 1]
        lines.append(f">{exc.lineno:>4} | {bad}")
        lines.append("     | " + " " * max(0, exc.colno - 1) + "^")
    return "\n".join(lines)


def _describe(value) -> str:
    if value is None:
        return "null"
    if isinstance(value, bool):
        return "true / false"
    if isinstance(value, int):
        return "整数"
    if isinstance(value, float):
        return "小数"
    if isinstance(value, str):
        return f"字符串（{len(value)} 字符）"
    if isinstance(value, list):
        return f"数组（{len(value)} 个元素）"
    if isinstance(value, dict):
        return f"对象（{len(value)} 个键）"
    return type(value).__name__


def _path_tokens(path: str):
    """把 items[2].name 拆成 ['items', 2, 'name']。"""
    tokens = []
    index = 0
    while index < len(path):
        ch = path[index]
        if ch == "[":
            end = path.find("]", index)
            if end == -1:
                raise ValueError("路径里的 [ 没有对应的 ]")
            inner = path[index + 1:end].strip().strip('"').strip("'")
            if not inner:
                raise ValueError("路径里有个空的 []")
            tokens.append(int(inner) if inner.lstrip("-").isdigit() else inner)
            index = end + 1
            continue
        if ch == "]":
            raise ValueError("路径里的 ] 没有对应的 [")
        if ch == ".":
            index += 1
            continue
        end = index
        while end < len(path) and path[end] not in ".[":
            end += 1
        name = path[index:end].strip()
        if name:
            tokens.append(int(name) if name.lstrip("-").isdigit() else name)
        index = end
    return tokens


def _walk(obj, path: str):
    tokens = _path_tokens(path)
    if not tokens:
        return obj
    current = obj
    walked = []
    for token in tokens:
        parent = ".".join(str(x) for x in walked) or "顶层"
        walked.append(token)
        if isinstance(token, int):
            if not isinstance(current, list):
                raise ValueError(f"{parent} 不是数组，取不到下标 {token}")
            if not -len(current) <= token < len(current):
                raise ValueError(f"{'.'.join(str(x) for x in walked)} 越界了（这个数组只有 {len(current)} 个元素）")
            current = current[token]
        else:
            if not isinstance(current, dict):
                raise ValueError(f"{parent} 不是对象，取不到键 {token}")
            if token not in current:
                keys = ", ".join(str(k) for k in list(current)[:10]) or "（一个键都没有）"
                raise ValueError(f"{parent} 里没有 {token} 这个键；有的是：{keys}")
            current = current[token]
    return current


def json_tool(data: str = "", op: str = "format", path: str = "", indent: int = 2) -> str:
    """JSON 美化 / 压缩 / 取值 / 校验。"""
    if not (data or "").strip():
        return "得给我一段 JSON 呀喵"
    if len(data) > MAX_TEXT:
        return f"JSON 太长了（{len(data)} 字符，最多 {MAX_TEXT}）"
    try:
        obj = json.loads(data)
    except json.JSONDecodeError as e:
        return _json_error(data, e)

    action = (op or "format").strip().lower()
    if action not in ("format", "minify", "get", "validate"):
        return f"不认识的 op：{op}（只有 format / minify / get / validate）"
    try:
        spaces = max(0, min(int(indent), 8))
    except (TypeError, ValueError):
        spaces = 2

    if action == "validate":
        return f"JSON 是合法的喵：顶层是{_describe(obj)}"

    if action == "get":
        if not path.strip():
            return "op=get 要一起给 path，比如 items[0].name"
        try:
            value = _walk(obj, path.strip())
        except ValueError as e:
            return f"取值失败：{e}"
        body = json.dumps(value, ensure_ascii=False, indent=spaces)
        return _clip(f"{path.strip()} 的值（{_describe(value)}）：\n{body}")

    if action == "minify":
        body = json.dumps(obj, ensure_ascii=False, separators=(",", ":"))
        return _clip(f"压成一行，{len(data)} → {len(body)} 字符：\n{body}")

    body = json.dumps(obj, ensure_ascii=False, indent=spaces)
    return _clip(f"顶层是{_describe(obj)}，缩进 {spaces} 空格：\n{body}")
