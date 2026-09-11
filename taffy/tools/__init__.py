"""工具注册表：汇总各模块的 SPECS，对上给模型一份 schema，对下按名字调函数。

新增工具只需要写一个模块，在里面放 SPECS 列表和同名函数，然后加进 _MODULES。
"""
import json

from . import basics, files, forensics, kb, runner, search, sticker

_MODULES = (basics, kb, search, files, forensics, runner, sticker)

TOOLS = []
TOOL_MAP = {}
for _module in _MODULES:
    for _spec in _module.SPECS:
        _name = _spec["function"]["name"]
        TOOLS.append(_spec)
        # 约定：工具名和函数名一致，直接按名字取
        TOOL_MAP[_name] = getattr(_module, _name)


def execute(name: str, raw_arguments: str):
    """执行一次工具调用，返回 (参数, 结果文本)。异常都转成结果文本，不往外抛。"""
    try:
        args = json.loads(raw_arguments or "{}")
    except json.JSONDecodeError:
        args = {}
    try:
        if name not in TOOL_MAP:
            return args, f"错误：没有名为 {name} 的工具"
        return args, str(TOOL_MAP[name](**args))
    except Exception as e:
        return args, f"工具 {name} 执行失败：{e}"
