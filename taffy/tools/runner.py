"""代码运行工具：只按扩展名挑解释器，不接受任意命令字符串，所以拼不出 shell 命令。"""
import locale
import os
import re
import subprocess
import sys
import tempfile

from ..config import CXX
from ..sandbox import WORKSPACE, safe_path
from . import _codescan

SPECS = [
    {
        "type": "function",
        "function": {
            "name": "run_code",
            "description": "编译并运行 workspace 里已有的代码文件，返回程序输出（含报错）。支持 .py / .js / .java / .cpp / .c，.java 和 C/C++ 会先编译再运行。运行目录固定为 workspace 根目录。所有语言都套了安全护栏：读写 workspace 以外的文件、联网、起进程、调用能操系统的库或命令都会被拦下并报错，路径只能写相对 workspace 的相对路径、不许用 .. 往上跑。所以代码就老老实实做纯计算，用什么库之前先想想它会不会碰文件或者网络。C/C++ 编译器是 TDM-GCC 4.9.2，只支持到 C++11：写 C++ 别用 C++14/17 的语法和标准库（没有 std::filesystem、没有结构化绑定、没有 auto 返回型别推导的简写），拿不准就用最基本的写法。",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "相对 workspace 的代码文件路径，例如 test.py",
                    },
                    "args": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "传给程序的命令行参数，可选",
                    },
                    "stdin": {
                        "type": "string",
                        "description": "程序的标准输入内容，可选",
                    },
                    "timeout": {
                        "type": "integer",
                        "description": "超时秒数，默认 20，最大 60",
                    },
                },
                "required": ["path"],
            },
        },
    },
]

_RUNNERS = {".js": ["node"]}

# Python 不是直接跑，而是先过一层审计钩子，越界操作当场被拦
_PY_GUARD = os.path.join(os.path.dirname(os.path.abspath(__file__)), "_pyguard.py")

# JS 没有钩子可用，改用 Node 自带的权限模型：只放开 workspace 的读写，
# 不给 --allow-child-process / --allow-worker / --allow-addons，这些就都用不了
_NODE_PERM = ["--permission", "--allow-fs-read=" + WORKSPACE, "--allow-fs-write=" + WORKSPACE]

# 子进程环境变量里这些字样的一律抹掉，免得模型能读到 API Key 之类的机密
_SECRET_ENV = ("KEY", "TOKEN", "SECRET", "PASSWORD", "PASSWD", "CREDENTIAL", "AUTH")

RUN_TIMEOUT = 20         # 默认超时秒数
RUN_MAX_TIMEOUT = 60     # 允许的最大超时
RUN_OUTPUT_LIMIT = 4000  # 输出字符上限


def _decode_line(raw: bytes) -> str:
    encodings = ["utf-8"]
    if os.name == "nt":
        encodings.append("mbcs")   # Windows 上是当前 ANSI 代码页，中文系统即 GBK
    encodings.append(locale.getpreferredencoding(False))
    for enc in dict.fromkeys(encodings):
        try:
            return raw.decode(enc)
        except (UnicodeDecodeError, LookupError):
            pass
    return raw.decode("utf-8", "replace")


def _decode(raw: bytes) -> str:
    """子进程输出可能是 utf-8，也可能是 Windows 本地编码（GBK），逐行试，
    这样一行解不开也不会把整段输出都带成乱码。"""
    text = "\n".join(_decode_line(line) for line in raw.split(b"\n"))
    return text.replace("\r\n", "\n")   # 统一换行符，免得 \r\n 和 \n 混着进上下文


def _exec(cmd: list, timeout: int, stdin: str = ""):
    """在 workspace 目录下执行命令，返回 (退出码, 输出)，超时连子进程一起杀"""
    env = {
        k: v for k, v in os.environ.items()
        if not any(word in k.upper() for word in _SECRET_ENV)
    }
    env["PYTHONIOENCODING"] = "utf-8"   # 让 python 子进程输出 utf-8，免得中文乱码
    env["PYTHONUTF8"] = "1"
    proc = subprocess.Popen(
        cmd,
        cwd=WORKSPACE,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        env=env,
        creationflags=subprocess.CREATE_NEW_PROCESS_GROUP if os.name == "nt" else 0,
    )
    try:
        out, _ = proc.communicate(input=stdin.encode("utf-8"), timeout=timeout)
        return proc.returncode, _decode(out)
    except subprocess.TimeoutExpired:
        if os.name == "nt":
            subprocess.run(["taskkill", "/F", "/T", "/PID", str(proc.pid)],
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        else:
            proc.kill()
        out, _ = proc.communicate()
        return None, f"运行超时（{timeout} 秒），进程已终止。\n{_decode(out or b'')}"


def _shorten(text: str) -> str:
    text = text.strip()
    if not text:
        return "（无输出）"
    if len(text) > RUN_OUTPUT_LIMIT:
        return text[:RUN_OUTPUT_LIMIT] + f"\n…（输出过长已截断，共 {len(text)} 字符）"
    return text


def _c_compiler(ext: str) -> str:
    """C++ 用 CXX（g++），C 用同目录的 gcc；CXX 只有名字没路径时就直接用名字"""
    if ext != ".c":
        return CXX
    name = "gcc.exe" if os.name == "nt" else "gcc"
    folder = os.path.dirname(CXX)
    return os.path.join(folder, name) if folder else name


def _run_c(full: str, ext: str, args: list, stdin: str, timeout: int) -> str:
    """C/C++ 先编译成临时可执行文件再运行，源文件留在 workspace 里不动"""
    with tempfile.TemporaryDirectory() as outdir:
        exe = os.path.join(outdir, "main.exe" if os.name == "nt" else "main")
        # -static 把 libstdc++ 静态链进去，否则运行时还得能找到编译器目录下的 dll
        cmd = [_c_compiler(ext), full, "-static", "-o", exe]
        if ext != ".c":
            cmd.insert(2, "-std=c++11")   # 这台机器的 g++ 4.9.2 默认还是 C++98，得手动指
        code, log = _exec(cmd, timeout)
        if code is None:
            return log
        if code != 0:
            return f"编译失败（退出码 {code}），先改代码：\n{_shorten(log)}"
        code, log = _exec([exe] + args, timeout, stdin)
    return log if code is None else f"编译通过，退出码 {code}\n{_shorten(log)}"


def run_code(path: str, args=None, stdin: str = "", timeout: int = RUN_TIMEOUT) -> str:
    """编译运行 workspace 内的代码文件并返回输出，支持 .py / .js / .java / .cpp / .c"""
    full = safe_path(path)
    if not os.path.isfile(full):
        return f"错误：文件不存在 {path}"

    if isinstance(args, str):       # 模型有时会把 args 传成一个字符串
        args = [args]
    args = [str(a) for a in (args or [])]
    try:
        timeout = max(1, min(int(timeout), RUN_MAX_TIMEOUT))
    except (TypeError, ValueError):
        timeout = RUN_TIMEOUT

    ext = os.path.splitext(full)[1].lower()

    # 非 Python 的几种语言跑起来就是原生进程，拦不住运行时行为，
    # 只能先静态审一遍源码，有危险调用直接不给跑
    blocked = _codescan.check(full, ext)
    if blocked:
        return blocked

    if ext == ".py":
        code, out = _exec(
            [sys.executable, _PY_GUARD, WORKSPACE, full] + args, timeout, stdin
        )
        return out if code is None else f"退出码 {code}\n{_shorten(out)}"

    if ext in _RUNNERS:
        perm = _NODE_PERM if ext in (".js", ".mjs") else []
        code, out = _exec(_RUNNERS[ext] + perm + [full] + args, timeout, stdin)
        return out if code is None else f"退出码 {code}\n{_shorten(out)}"

    if ext in (".cpp", ".cc", ".cxx", ".c"):
        return _run_c(full, ext, args, stdin, timeout)

    if ext == ".java":
        with tempfile.TemporaryDirectory() as outdir:
            code, log = _exec(["javac", "-encoding", "UTF-8", "-d", outdir, full], timeout)
            if code is None:
                return log
            if code != 0:
                return f"编译失败（退出码 {code}），先改代码：\n{_shorten(log)}"
            with open(full, "r", encoding="utf-8", errors="replace") as f:
                m = re.search(r"class\s+(\w+)", f.read())
            cls = m.group(1) if m else os.path.splitext(os.path.basename(full))[0]
            code, log = _exec(["java", "-Dfile.encoding=UTF-8",
                               "-Dstdout.encoding=UTF-8", "-Dstderr.encoding=UTF-8",
                               "-cp", outdir, cls] + args, timeout, stdin)
        return log if code is None else f"编译通过，退出码 {code}\n{_shorten(log)}"

    return f"错误：不支持运行 {ext or '无扩展名'} 文件，目前只支持 .py / .js / .java / .cpp / .c"
