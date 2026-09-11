"""非 Python 代码的跑前安全审查。

Python 那边靠 _pyguard.py 的审计钩子做运行时拦截；C/C++/Java/JS 是原生进程，
挂不上钩子，所以改成跑之前先把源码静态审一遍：危险的头文件 / 包 / 函数、
指向 workspace 外面或者往上级目录跑的路径字符串，命中就直接不给跑。
JS 另有一层 Node 自带的权限模型兜底，文件读写锁死在 workspace。

说清楚它的边界：静态审查拦得住「模型手滑写出危险代码」，拦不住处心积虑的绕过。
它是护栏，不是保险柜。
"""
import os
import re

# ---------- 源码预处理 ----------


def _strip_comments(text):
    """去掉 // 和 /* */ 注释，注释改成等长空白，字符串原样保留。"""
    out = []
    i, n = 0, len(text)
    while i < n:
        c = text[i]
        if c in "\"'`":
            quote = c
            out.append(c)
            i += 1
            while i < n:
                d = text[i]
                i += 1
                if d == "\\" and i < n:
                    out.append(d)
                    out.append(text[i])
                    i += 1
                    continue
                out.append(d)
                if d == quote:
                    break
            continue
        if c == "/" and i + 1 < n and text[i + 1] == "/":
            while i < n and text[i] != "\n":
                out.append(" ")
                i += 1
            continue
        if c == "/" and i + 1 < n and text[i + 1] == "*":
            i += 2
            out.append("  ")
            while i < n and not (text[i] == "*" and i + 1 < n and text[i + 1] == "/"):
                out.append("\n" if text[i] == "\n" else " ")
                i += 1
            if i < n:
                out.append("  ")
                i += 2
            continue
        out.append(c)
        i += 1
    return "".join(out)


def _blank_strings(text):
    """把字符串内容涂成空白，只留引号。

    不然题目里出现一个 "system(" 这样的字符串就会被误判成真的在调 system()。
    """
    out = []
    i, n = 0, len(text)
    while i < n:
        c = text[i]
        if c in "\"'`":
            quote = c
            i += 1
            while i < n:
                d = text[i]
                i += 1
                if d == "\\" and i < n:
                    i += 1
                    continue
                if d == quote:
                    break
            out.append(quote)
            out.append(quote)
            continue
        out.append(c)
        i += 1
    return "".join(out)


# ---------- 路径字符串 ----------

_PATH_RULES = (
    (re.compile(r"""["'`][A-Za-z]:[\\/]"""), "写死的绝对路径"),
    (re.compile(r"""["'`]\\\\{2,}"""), "UNC 网络路径"),
    (re.compile(r"""["'`]\.\.[\\/]"""), "往上级目录跑的相对路径"),
    (re.compile(r"""["'`]/(?:etc|home|root|proc|sys|dev|usr|var|tmp|boot)/"""), "系统目录"),
)


def _path_hit(paths_text):
    for pattern, why in _PATH_RULES:
        m = pattern.search(paths_text)
        if m:
            return f"{why}：{m.group(0)[1:]}"
    return None


# ---------- C / C++ ----------

# 这些头文件在算法题里几乎不可能正当出现，出现就是想在系统层面动手
_C_HEADERS = re.compile(
    r"""#\s*include\s*[<"]\s*("""
    r"""windows|winsock2|ws2tcpip|shellapi|winreg|tlhelp32|shlobj|process|direct|"""
    r"""winbase|winsvc|userenv|lz32|urlmon|sys/socket|netinet/in|arpa/inet|dlfcn"""
    r""")\s*[>"]""",
    re.I,
)

_C_FUNCS = re.compile(
    r"""\b("""
    r"""system|_wsystem|popen|_popen|"""
    r"""execl|execle|execlp|execlpe|execv|execve|execvp|execvpe|fork|"""
    r"""unlink|_unlink|rmdir|_rmdir|_chdir|chmod|_chmod|"""
    r"""WinExec|ShellExecute|CreateProcess|TerminateProcess|OpenProcess|"""
    r"""WriteProcessMemory|ReadProcessMemory|CreateRemoteThread|VirtualAllocEx|"""
    r"""DeleteFile|RemoveDirectory|MoveFileEx|CopyFile|SetFileAttributes|"""
    r"""RegOpenKey|RegSetValue|RegCreateKey|RegDeleteKey|"""
    r"""LoadLibrary|GetProcAddress|URLDownloadToFile|InternetOpen|InternetReadFile|"""
    r"""WSAStartup|gethostbyname|inet_addr"""
    r""")\s*\(""",
    re.I,
)

_C_ASM = re.compile(r"\b(__asm__|__asm|asm)\b\s*(volatile\s*)?[\({]")

_C_RULES = (
    # 头文件要连着字符串一起看，因为 #include "windows.h" 的引号里就是模块名
    (_C_HEADERS, "用到了能直接操作系统的头文件", "stripped"),
    (_C_ASM, "用了内联汇编", "code"),
    (_C_FUNCS, "调用了能起进程 / 删文件 / 联网 / 改系统的函数", "code"),
)


# ---------- Java ----------

_JAVA_RULES = (
    (re.compile(r"\bRuntime\s*\.\s*getRuntime\s*\("), "Runtime.getRuntime() 能起外部进程", "code"),
    (re.compile(r"\bnew\s+ProcessBuilder\b|\bProcessBuilder\b"), "ProcessBuilder 能起外部进程", "code"),
    (re.compile(r"\bnew\s+File\s*\(|\bjava\s*\.\s*io\s*\.\s*File\b"), "File 能读写任意路径", "code"),
    (re.compile(
        r"\bnew\s+(FileWriter|FileReader|FileOutputStream|FileInputStream|"
        r"RandomAccessFile|FileChannel)\b"
    ), "文件流能读写任意路径", "code"),
    (re.compile(r"\bjava\s*\.\s*nio\s*\.\s*file\b"), "java.nio.file 能读写任意路径", "code"),
    (re.compile(
        r"\b(Files|Paths)\s*\.\s*(get|readAllBytes|readAllLines|readString|write|writeString|"
        r"newInputStream|newOutputStream|newBufferedReader|newBufferedWriter|delete|"
        r"deleteIfExists|move|copy|createDirectories|createFile|createTempFile|walk|list)"
    ), "java.nio 的文件操作能读写任意路径", "code"),
    (re.compile(r"\bnew\s+(Socket|ServerSocket|DatagramSocket)\s*\("), "套接字能联网", "code"),
    (re.compile(r"\bjava\s*\.\s*net\s*\."), "java.net 能联网", "code"),
    (re.compile(r"\b(URLConnection|HttpURLConnection|HttpClient|InetAddress)\b"), "网络类能联网", "code"),
    (re.compile(r"\b(ScriptEngineManager|Unsafe)\b"), "脚本引擎 / Unsafe 能绕过限制", "code"),
    (re.compile(r"\bSystem\s*\.\s*(load|loadLibrary|setSecurityManager)\s*\("),
     "能加载原生库或关掉安全限制", "code"),
)


# ---------- JavaScript ----------

_JS_MODULES = (
    "child_process|net|http|https|http2|dgram|tls|cluster|worker_threads|"
    "vm|v8|wasi|repl|inspector|module|os|process"
)

_JS_RULES = (
    # 模块名就写在引号里，所以这条得看没涂白字符串的版本
    (re.compile(
        r"""(?:require\s*\(\s*|from\s+|import\s*\(\s*)["'`](?:node:)?(""" + _JS_MODULES + r""")["'`]"""
    ), "引入了能起进程 / 联网 / 绕过限制的模块", "stripped"),
    (re.compile(r"\bprocess\s*\.\s*(kill|binding|dlopen|setuid|setgid)\s*\("),
     "危险的 process 调用", "code"),
)


_RULES = {
    ".c": _C_RULES,
    ".cc": _C_RULES,
    ".cpp": _C_RULES,
    ".cxx": _C_RULES,
    ".java": _JAVA_RULES,
    ".js": _JS_RULES,
    ".mjs": _JS_RULES,
}


def check(path: str, ext: str) -> str:
    """审一遍源码。不安全就返回给模型的说明，安全就返回空字符串。"""
    rules = _RULES.get(ext)
    if not rules:
        return ""

    with open(path, "r", encoding="utf-8", errors="replace") as f:
        raw = f.read()

    stripped = _strip_comments(raw)
    code = _blank_strings(stripped)
    texts = {"stripped": stripped, "code": code}

    for pattern, why, target in rules:
        m = pattern.search(texts[target])
        if m:
            return (
                f"安全拦截：{why}喵（命中 `{m.group(0).strip()}`）。"
                f"塔菲的代码只准在 workspace 里做纯计算，不联网、不起进程、不碰 workspace 以外的文件。"
                f"改掉这段再用 run_code 重新跑喵。"
            )

    hit = _path_hit(stripped)
    if hit:
        return (
            f"安全拦截：{hit}喵。塔菲的代码只能读写 workspace 里的文件，"
            f"路径要写相对 workspace 的相对路径，也不许用 .. 往上跑。改掉再用 run_code 跑喵。"
        )

    return ""
