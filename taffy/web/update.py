"""检查更新 / 一键更新：从 Gitee 或 GitHub 拉最新版，拉完自动重启。

只对「git clone 部署出来的目录」有用——后台就跑在这个仓库里，直接拿它自己的 git
仓库当更新源。默认 Gitee：国内服务器连 GitHub 经常直接超时（这台就是）。

更新完得重启才生效，所以拉完隔两秒去调 systemctl 重启自己——先让 HTTP 响应发出去，
再让 systemd 用新代码把进程拉起来。不是 systemd 管的话就老实告诉主人「你自己重启」。

任何一步失败都只报错不折腾：绝不 stash、绝不 reset、绝不用 --force。
"""
import os
import subprocess
import threading

from ..config import PROJECT_ROOT, SERVICE_NAME

TIMEOUT = 120
# 要密码就直接失败，别把后台请求挂在那儿等输入（服务器上的仓库是公开的，用不着密码）
_ENV = dict(os.environ, GIT_TERMINAL_PROMPT="0")


def _run(args, timeout=TIMEOUT):
    """跑一条命令，返回 (是否成功, 输出)。"""
    try:
        proc = subprocess.run(
            args, cwd=PROJECT_ROOT, env=_ENV,
            stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
            timeout=timeout,
        )
    except FileNotFoundError:
        return False, f"这台机器上找不到 {args[0]}"
    except subprocess.TimeoutExpired:
        return False, f"{' '.join(args)} 超时了（{timeout} 秒），大概是连不上那个远端"
    except OSError as exc:
        return False, f"命令跑不起来：{exc}"
    return proc.returncode == 0, proc.stdout.decode("utf-8", "replace").strip()


def _git(*args, **kwargs):
    return _run(["git", *args], **kwargs)


def remotes():
    """仓库里配了哪些远端：{名字: 地址}。"""
    ok, out = _git("remote", "-v")
    if not ok:
        return {}
    found = {}
    for line in out.splitlines():
        parts = line.split()
        if len(parts) >= 2:
            found.setdefault(parts[0], parts[1])
    return found


def pick_remote(provider):
    """按厂家挑远端（地址里带 gitee.com / github.com 的那个）。没有就返回空。"""
    for name, url in remotes().items():
        if provider == "gitee" and "gitee.com" in url:
            return name, url
        if provider == "github" and "github.com" in url:
            return name, url
    return "", ""


def _branch():
    ok, out = _git("rev-parse", "--abbrev-ref", "HEAD")
    return out if ok else ""


def service_active():
    """服务是不是 systemd 在管（是的话更新完能自动重启）。"""
    if not SERVICE_NAME:
        return False
    try:
        proc = subprocess.run(
            ["systemctl", "is-active", SERVICE_NAME],
            stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, timeout=10,
        )
    except (OSError, subprocess.TimeoutExpired):
        return False
    return proc.stdout.decode("utf-8", "replace").strip() == "active"


def check(provider):
    """看看远端有没有新东西。全程只读，不碰工作区。"""
    info = {
        "provider": provider,
        "remote": "",
        "url": "",
        "branch": _branch(),
        "local": "",
        "remote_head": "",
        "behind": 0,
        "commits": [],
        "up_to_date": False,
        "error": "",
        "can_auto_restart": service_active(),
        "service": SERVICE_NAME,
    }
    name, url = pick_remote(provider)
    info["remote"], info["url"] = name, url
    if not name:
        have = "、".join(remotes().keys()) or "一个都没有"
        info["error"] = f"这个仓库里没有 {provider} 的远端地址（现有远端：{have}），换一个厂家试试"
        return info
    if not info["branch"] or info["branch"] == "HEAD":
        info["error"] = "当前不在任何分支上（detached HEAD），没法比较"
        return info

    ok, out = _git("rev-parse", "HEAD")
    info["local"] = out[:8] if ok else ""

    ok, out = _git("fetch", name, "--prune", "--quiet")
    if not ok:
        info["error"] = f"拉取远端仓库信息失败：{out[-300:]}"
        return info

    ref = f"{name}/{info['branch']}"
    ok, out = _git("rev-parse", ref)
    if not ok:
        info["error"] = f"远端没有 {ref} 这个分支"
        return info
    info["remote_head"] = out[:8]

    ok, out = _git("rev-list", "--count", f"HEAD..{ref}")
    if ok and out.isdigit():
        info["behind"] = int(out)
    ok, out = _git("log", "--oneline", "--no-decorate", "-n", "20", f"HEAD..{ref}")
    if ok and out:
        info["commits"] = out.splitlines()
    info["up_to_date"] = info["behind"] == 0
    return info


def _restart_later(delay=2.0):
    """过一会儿重启服务：先让响应发回去，再让 systemd 把新代码拉起来。"""
    timer = threading.Timer(delay, _restart_now)
    timer.daemon = True
    timer.start()


def _restart_now():
    # --no-block：任务交给 systemd 就返回，免得自己被杀在半路。
    # start_new_session：别跟本进程一个会话，不然一起被带走。
    for cmd in (["systemctl", "--no-block", "restart", SERVICE_NAME],
                ["systemctl", "restart", SERVICE_NAME]):
        try:
            subprocess.Popen(cmd, start_new_session=True,
                             stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            return
        except OSError:
            continue


def apply(provider):
    """拉最新版。成功的话顺手安排一次重启。"""
    name, url = pick_remote(provider)
    if not name:
        return {"ok": False, "message": f"这个仓库里没有 {provider} 的远端地址，拉不了", "restart": False}
    branch = _branch()
    if not branch or branch == "HEAD":
        return {"ok": False, "message": "当前不在任何分支上，拉不了", "restart": False}

    before, _ = _git("rev-parse", "--short", "HEAD")
    ok, out = _git("pull", "--ff-only", name, branch)
    if not ok:
        return {
            "ok": False,
            "restart": False,
            "message": "拉取失败（本地改过文件、或者历史分叉了）。这条命令只在能快进时才动，"
                       "本地改动一律不覆盖，需要的话上服务器手动处理：" + out[-300:],
        }
    after, _ = _git("rev-parse", "--short", "HEAD")
    if before == after:
        return {"ok": True, "restart": False, "from": before, "to": after,
                "message": f"已经是最新的了（{after}），没有东西要更新"}

    if service_active():
        _restart_later()
        return {
            "ok": True, "restart": True, "from": before, "to": after,
            "message": f"更新好了：{before} → {after}。两秒后自动重启生效，"
                       f"页面会短暂断一下，刷新就好（systemctl 服务名 {SERVICE_NAME}）。",
        }
    return {
        "ok": True, "restart": False, "from": before, "to": after,
        "message": f"代码更新好了：{before} → {after}。但没检测到 systemd 在管 {SERVICE_NAME} 这个服务，"
                   "没法自动重启，自己重启一下才生效喵。",
    }