"""联网工具：搜资料，以及打开链接读正文。

搜索用 360 搜索（so.com）：国内可直连、免密钥，中文时效性查询的相关性比必应好很多。
open_url 负责把网页正文抓回来，只认 http/https，本机和内网地址不给开。
"""
import html
import ipaddress
import re
import socket
from urllib.parse import urljoin, urlsplit

import charset_normalizer
import lxml.etree
import lxml.html
import requests

SPECS = [
    {
        "type": "function",
        "function": {
            "name": "web_search",
            "description": "联网搜索资料，返回标题、链接和摘要",
            "parameters": {
                "type": "object",
                "properties": {
                    "keyword": {
                        "type": "string",
                        "description": "搜索关键词",
                    },
                    "max_results": {
                        "type": "integer",
                        "description": "返回条数，默认 5，最多 10",
                    },
                },
                "required": ["keyword"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "open_url",
            "description": (
                "打开一个 http/https 链接，把网页正文抓回来读。"
                "雏草姬甩过来一个网址、或者搜索/知识库结果里有想细看的页面时用这个。"
                "返回的是网页正文纯文本；打不开、或者不是网页（图片、压缩包之类）会直接说明。"
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "url": {
                        "type": "string",
                        "description": "要打开的完整网址，要带 http:// 或 https://",
                    },
                },
                "required": ["url"],
            },
        },
    },
]

SEARCH_URL = "https://www.so.com/s"
SEARCH_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
}
# so.com 直连即可，走系统代理反而会被拒
NO_PROXY = {"http": None, "https": None}
TITLE_RE = re.compile(
    r'<h3[^>]*class="[^"]*res-title[^"]*"[^>]*>\s*'
    r'<a[^>]*href="([^"]+)"[^>]*>(.*?)</a>',
    re.S,
)
SNIPPET_RE = re.compile(r'<p[^>]*class="[^"]*res-desc[^"]*"[^>]*>(.*?)</p>', re.S)


def _clean(text: str) -> str:
    return html.unescape(re.sub(r"<.*?>", "", text)).strip()


def web_search(keyword: str, max_results: int = 5) -> str:
    """用 360 搜索，返回标题 / 链接 / 摘要"""
    try:
        resp = requests.get(
            SEARCH_URL,
            params={"q": keyword},
            headers=SEARCH_HEADERS,
            proxies=NO_PROXY,
            timeout=20,
        )
        resp.raise_for_status()
    except Exception as e:
        return f"搜索失败：{e}"

    # 摘要跟在标题后面，取标题之后的一小段窗口来找，避免被嵌套标签截断
    page = resp.text
    results = []
    for m in TITLE_RE.finditer(page):
        snippet = SNIPPET_RE.search(page[m.end(): m.end() + 2000])
        results.append(
            {
                "title": _clean(m.group(2)),
                "url": html.unescape(m.group(1)),
                "snippet": _clean(snippet.group(1)) if snippet else "",
            }
        )
        if len(results) >= max(1, min(max_results, 10)):
            break

    if not results:
        return f"没有搜到「{keyword}」的结果"
    return "\n\n".join(
        f"{i}. {r['title']}\n   {r['url']}\n   {r['snippet']}"
        for i, r in enumerate(results, 1)
    )


# ---------------- 打开链接 ----------------

FETCH_HEADERS = {
    "User-Agent": SEARCH_HEADERS["User-Agent"],
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
}

MAX_BYTES = 2 * 1024 * 1024   # 最多下 2MB，免得被超长页面拖死
MAX_CHARS = 6000              # 正文最多回这么多字，再长就截断
MAX_REDIRECTS = 5             # 最多跟 5 跳，每一跳都重新查一遍地址
DROP_TAGS = ("script", "style", "noscript", "svg", "iframe", "form",
             "nav", "footer", "header", "aside", "template", "button")
BLOCK_END = re.compile(
    r"</(?:p|div|li|tr|h[1-6]|section|article|blockquote|pre|table|ul|ol)\s*>|<br\s*/?>",
    re.I,
)
TAG_RE = re.compile(r"<[^>]*>")
BLANK_RE = re.compile(r"\n{3,}")
SPACE_RE = re.compile(r"[ \t\u00a0]+")
CHARSET_RE = re.compile(rb"""charset\s*=\s*["']?([\w-]+)""", re.I)


def _host_blocked(host: str) -> bool:
    """本机、内网、保留地址一律不给开，免得拿塔菲当跳板去戳内部服务"""
    if not host:
        return True
    host = host.lower().strip("[]")
    if host == "localhost" or host.endswith((".local", ".internal", ".localhost")):
        return True
    try:
        infos = socket.getaddrinfo(host, None)
    except OSError:
        return False        # 解析不了就交给 requests 去报错，这里不拦
    for info in infos:
        try:
            ip = ipaddress.ip_address(info[4][0])
        except ValueError:
            continue
        # is_global 把私网、回环、链路本地、保留、CGNAT(100.64/10) 这些都算作
        # 非全局，一次挡掉；组播地址它却算全局，所以另判一下
        if not ip.is_global or ip.is_multicast:
            return True
    return False


def _check_url(url: str):
    """只认 http/https，且不能是本机/内网。合法返回 None，否则返回拒绝说明。"""
    parsed = urlsplit(url)
    if parsed.scheme.lower() not in ("http", "https"):
        return f"只认 http / https 的链接喵，{parsed.scheme or '这种'}开头的不给开"
    if _host_blocked(parsed.hostname):
        return "这个地址指向本机或者内网，塔菲不给开喵"
    return None


def _fetch(url: str):
    """自己一跳一跳跟重定向，每一跳都重新校验地址。

    交给 requests 自动跟的话，它只看得到第一跳的地址，公网页面 302 到 127.0.0.1
    这种就绕过去了。这里关掉自动跳转，自己走，每跳都查一遍。
    返回 (错误说明, 响应)，错误说明非空时响应为 None。
    """
    for hop in range(MAX_REDIRECTS + 1):
        bad = _check_url(url)
        if bad:
            if hop == 0:
                return bad, None
            return f"链接跳转到了不给开的地方（{url}），塔菲就不跟了喵。{bad}", None
        try:
            resp = requests.get(url, headers=FETCH_HEADERS, timeout=20,
                                stream=True, allow_redirects=False)
        except Exception as e:
            return f"打不开这个链接：{e}", None
        location = resp.headers.get("Location")
        if resp.status_code in (301, 302, 303, 307, 308) and location:
            resp.close()
            url = urljoin(url, location)
            continue
        return None, resp
    return "这个链接跳来跳去太多次了，塔菲不跟了喵", None


def _decode(raw: bytes, resp) -> str:
    """猜编码。requests 对没写 charset 的网页会给 iso-8859-1，那个基本是错的，不认。"""
    enc = resp.encoding
    if enc and enc.lower() in ("iso-8859-1", "ascii"):
        enc = None
    if not enc:
        m = CHARSET_RE.search(raw[:4096])
        enc = m.group(1).decode("ascii", "ignore") if m else None
    if not enc:
        best = charset_normalizer.from_bytes(raw).best()
        enc = str(best.encoding) if best else "utf-8"
    try:
        return raw.decode(enc, errors="replace")
    except LookupError:
        return raw.decode("utf-8", errors="replace")


def _pick_main(doc):
    """挑正文。正文块里的 <p> 总字数一般最多，取它；都不像正文就退回整个文档。"""
    best, best_len = None, 0
    for node in doc.iter("article", "main", "div", "section"):
        length = sum(len(p.text_content()) for p in node.iter("p"))
        if length > best_len:
            best, best_len = node, length
    return best if best_len >= 200 else doc


def _html_to_text(markup: str) -> str:
    try:
        doc = lxml.html.fromstring(markup)
    except Exception:
        return ""
    lxml.etree.strip_elements(doc, *DROP_TAGS, with_tail=False)
    node = _pick_main(doc)
    out = lxml.etree.tostring(node, encoding="unicode", method="html")
    out = BLOCK_END.sub("\n", out)
    out = html.unescape(TAG_RE.sub("", out))
    out = SPACE_RE.sub(" ", out)
    out = "\n".join(line.strip() for line in out.splitlines())
    return BLANK_RE.sub("\n\n", out).strip()


def open_url(url: str, max_chars: int = MAX_CHARS) -> str:
    """打开一个网址，把网页正文抓回来"""
    url = (url or "").strip()
    if not url:
        return "没给网址喵"

    err, resp = _fetch(url)
    if err:
        return err

    with resp:
        if resp.status_code >= 400:
            return f"打不开这个链接：HTTP {resp.status_code}"
        ctype = (resp.headers.get("Content-Type") or "").lower()
        chunks, total = [], 0
        try:
            for chunk in resp.iter_content(8192):
                chunks.append(chunk)
                total += len(chunk)
                if total >= MAX_BYTES:
                    break
        except Exception as e:
            return f"读这个链接的时候断了：{e}"

    raw = b"".join(chunks)
    cut = total >= MAX_BYTES

    if "pdf" in ctype:
        return "这个链接是 PDF，塔菲没法直接读正文喵。想读的话下下来放进 knowledge/ 目录，塔菲就能索引了"
    if ctype and not any(k in ctype for k in ("html", "text", "json", "xml")):
        return f"这个链接不是网页（{ctype.split(';')[0]}），塔菲打开也读不了喵"

    text = _decode(raw, resp)
    if "html" in ctype or "<html" in text[:2000].lower():
        text = _html_to_text(text)
    if not text.strip():
        return "网页打开了，但里面没抓到正文喵（可能是纯图片页或者要登录）"

    text = text.strip()
    if len(text) > max_chars:
        text = text[:max_chars] + "\n\n……（正文太长，塔菲先看到这儿）"
    elif cut:
        text += "\n\n……（网页太大，只下了前 2MB）"
    return text

