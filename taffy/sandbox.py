"""工作区沙箱：把所有文件操作限制在 workspace 目录内。"""
import os

from .config import PROJECT_ROOT

WORKSPACE = os.path.realpath(os.path.join(PROJECT_ROOT, "workspace"))
os.makedirs(WORKSPACE, exist_ok=True)


def safe_path(path: str) -> str:
    """把相对路径解析成 workspace 内的绝对路径，越界就抛 ValueError。

    比较时两边都过一遍 normcase：Windows 文件系统不区分大小写，而 IDE 传进来的
    __file__ 可能是小写盘符 f:\\，realpath 返回的却是大写 F:\\，直接比字符串会误判越界。
    """
    full = os.path.realpath(os.path.join(WORKSPACE, path))
    root = os.path.normcase(WORKSPACE)
    target = os.path.normcase(full)
    if target != root and not target.startswith(root + os.sep):
        raise ValueError(f"路径超出工作区，只能操作 workspace 下的文件：{path}")
    return full
