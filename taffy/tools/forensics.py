"""数字取证工具：哈希校验、文件类型识别、字符串提取、文件雕复、时间戳与元数据。

只用标准库（PDF 元数据复用已有的 pypdf），不联网、不起子进程。输入输出都走
safe_path 锁在 workspace 内。除 carve_files 会把雕复出来的文件写进 workspace 外，
其余工具只读样本、以文字报告返回。
"""
import datetime
import hashlib
import math
import os
import re
import struct

from ..sandbox import safe_path

# 单个样本最多读这么多，防止一个巨型文件把内存吃光
_MAX_READ = 128 * 1024 * 1024
# 雕复时没有可靠结尾标记的格式，最多往后取这么大
_MAX_CARVE_SIZE = 8 * 1024 * 1024
# 熵值只在文件开头采这么多字节，全量统计太慢
_ENTROPY_SAMPLE = 256 * 1024

SPECS = [
    {
        "type": "function",
        "function": {
            "name": "hash_file",
            "description": "计算 workspace 里某个文件的 MD5 / SHA1 / SHA256（取证第一步的完整性校验）。可传 expected 跟已有哈希比对，判断文件有没有被动过。",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "相对 workspace 的文件路径，例如 samples/case.jpg"},
                    "expected": {"type": "string", "description": "可选。已知的哈希值，用来比对是否一致（自动忽略大小写和空格）"},
                },
                "required": ["path"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "identify_file",
            "description": "读文件头魔数判断文件真实类型，并和扩展名比对（能看出改后缀伪装的文件）；同时给出大小、时间戳和熵值（熵接近 8 说明是加密 / 压缩 / 打包过的）。",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "相对 workspace 的文件路径"},
                },
                "required": ["path"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "extract_strings",
            "description": "从二进制文件里提取可打印字符串（ASCII、UTF-16LE、中文都认），带偏移量。找 flag、URL、路径、命令、邮箱、密钥时用这个。可用 keyword 只筛含关键字的行。",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "相对 workspace 的文件路径"},
                    "min_len": {"type": "integer", "description": "最短字符串长度，默认 4"},
                    "keyword": {"type": "string", "description": "可选。只返回包含该关键字的字符串（不区分大小写）"},
                    "limit": {"type": "integer", "description": "最多返回多少条，默认 200"},
                },
                "required": ["path"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "carve_files",
            "description": "文件雕复：从二进制文件（镜像、被删过内容的文件）里按文件头尾签名把里面嵌的图片 / PDF / 压缩包等抠出来，写到 workspace 下的 out_dir。用于恢复被删除或藏在文件里的内容。",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "相对 workspace 的样本文件路径"},
                    "out_dir": {"type": "string", "description": "雕复结果写到 workspace 下的哪个目录，默认 carved"},
                    "max_files": {"type": "integer", "description": "最多雕复几个文件，默认 50"},
                },
                "required": ["path"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "file_metadata",
            "description": "看文件的创建 / 修改 / 访问时间（MACB 时间线），以及文档元数据：PDF 的作者 / 制作软件 / 生成时间，JPEG 的 EXIF（相机型号、拍摄时间、GPS 经纬度）。",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "相对 workspace 的文件路径"},
                },
                "required": ["path"],
            },
        },
    },
]

# 文件头魔数 -> (类型描述, 常见扩展名)。同一种类型按特征从长到短排，先匹配长的。
_SIGNATURES = (
    (b"\x89PNG\r\n\x1a\n", "PNG 图片", ".png"),
    (b"SQLite format 3\x00", "SQLite 数据库", ".sqlite/.db"),
    (b"\xd0\xcf\x11\xe0\xa1\xb1\x1a\xe1", "旧版 Office 文档 / OLE2 复合文档（doc/xls/ppt/msg）", ".doc/.xls/.ppt"),
    (b"\x7fELF", "Linux 可执行文件（ELF）", ""),
    (b"Rar!\x1a\x07", "RAR 压缩包", ".rar"),
    (b"7z\xbc\xaf\x27\x1c", "7-Zip 压缩包", ".7z"),
    (b"PK\x03\x04", "ZIP 容器（也可能是 docx / xlsx / jar / apk）", ".zip"),
    (b"PK\x05\x06", "ZIP 空包（只有目录）", ".zip"),
    (b"\xff\xd8\xff", "JPEG 图片", ".jpg"),
    (b"GIF87a", "GIF 图片", ".gif"),
    (b"GIF89a", "GIF 图片", ".gif"),
    (b"%PDF", "PDF 文档", ".pdf"),
    (b"\x1f\x8b", "GZIP 压缩流", ".gz"),
    (b"BZh", "BZIP2 压缩流", ".bz2"),
    (b"\xca\xfe\xba\xbe", "Java class / Mach-O 通用二进制", ".class"),
    (b"OggS", "Ogg 媒体", ".ogg"),
    (b"ID3", "MP3 音频（带 ID3 标签）", ".mp3"),
    (b"RIFF", "RIFF 容器（WAV / AVI / WebP）", ".wav/.avi/.webp"),
    (b"MZ", "Windows 可执行文件（EXE / DLL）", ".exe/.dll"),
    (b"BM", "BMP 位图", ".bmp"),
)

# 雕复签名：(扩展名, 头, 尾)。尾为 None 的格式没有可靠结束标记，按 _MAX_CARVE_SIZE 截。
_CARVE_SIGNATURES = (
    ("jpg", b"\xff\xd8\xff", b"\xff\xd9"),
    ("png", b"\x89PNG\r\n\x1a\n", b"IEND\xaeB`\x82"),
    ("gif", b"GIF89a", b"\x00\x3b"),
    ("pdf", b"%PDF", b"%%EOF"),
    ("zip", b"PK\x03\x04", None),
)

_EXIF_IFD0 = {
    0x010F: "相机厂商",
    0x0110: "相机型号",
    0x0112: "方向",
    0x0131: "处理软件",
    0x0132: "拍摄时间",
    0x013B: "作者",
    0x8298: "版权",
}
_GPS_NAMES = {1: "GPS 纬度", 2: "GPS 纬度", 3: "GPS 经度", 4: "GPS 经度", 6: "GPS 海拔"}


def _read(path):
    """读样本文件，超过上限就只读前半部分。"""
    full = safe_path(path)
    if not os.path.isfile(full):
        raise ValueError(f"文件不存在 {path}")
    if os.path.getsize(full) <= _MAX_READ:
        with open(full, "rb") as f:
            return f.read(), False
    with open(full, "rb") as f:
        return f.read(_MAX_READ), True


def hash_file(path: str, expected: str = "") -> str:
    """算 MD5 / SHA1 / SHA256，可选与 expected 比对。"""
    full = safe_path(path)
    if not os.path.isfile(full):
        return f"错误：文件不存在 {path}"

    digests = {name: hashlib.new(name) for name in ("md5", "sha1", "sha256")}
    size = 0
    with open(full, "rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            size += len(block)
            for hasher in digests.values():
                hasher.update(block)

    lines = [f"文件：{path}", f"大小：{size} 字节"]
    for name, hasher in digests.items():
        lines.append(f"{name.upper()}：{hasher.hexdigest()}")

    if expected:
        want = expected.strip().lower().replace(" ", "")
        matched = [name.upper() for name, hasher in digests.items() if hasher.hexdigest() == want]
        if matched:
            lines.append(f"比对结果：与 expected 一致（命中 {matched[0]}）")
        else:
            lines.append("比对结果：不一致！文件可能被修改过，或者 expected 传错了")
    return "\n".join(lines)


def _entropy(data):
    """香农熵，采样前 _ENTROPY_SAMPLE 字节。"""
    sample = data[:_ENTROPY_SAMPLE]
    if not sample:
        return 0.0
    counts = {}
    for byte in sample:
        counts[byte] = counts.get(byte, 0) + 1
    total = len(sample)
    return -sum((c / total) * math.log2(c / total) for c in counts.values())


def _identify(data):
    """按魔数猜类型，认不出来再看是不是纯文本。"""
    for magic, desc, ext in _SIGNATURES:
        if data.startswith(magic):
            return desc, ext
    sample = data[:4096]
    if sample and b"\x00" not in sample:
        for encoding in ("utf-8", "gbk"):
            try:
                sample.decode(encoding)
                return f"纯文本（{encoding}）", ".txt"
            except UnicodeDecodeError:
                continue
    return "未知格式", ""


def identify_file(path: str) -> str:
    """魔数识别 + 扩展名比对 + 熵值。"""
    data, truncated = _read(path)
    size = os.path.getsize(safe_path(path))
    desc, ext = _identify(data)
    entropy = _entropy(data)

    lines = [
        f"文件：{path}",
        f"大小：{size} 字节",
        f"实际类型：{desc}",
    ]
    if ext:
        lines.append(f"这类文件常用扩展名：{ext}")

    real_ext = os.path.splitext(path)[1].lower().lstrip(".")
    if real_ext and ext:
        allowed = [e.lstrip(".").lower() for e in ext.split("/")]
        if real_ext not in allowed:
            lines.append(f"⚠ 扩展名是 .{real_ext}，但内容其实是 {desc}——疑似改后缀伪装")

    note = "加密 / 压缩 / 打包过" if entropy > 7.5 else ("基本是明文" if entropy < 5.5 else "普通二进制数据")
    lines.append(f"熵值：{entropy:.2f} / 8（采样前 {_ENTROPY_SAMPLE // 1024}KB，{note}）")
    if truncated:
        lines.append(f"注意：文件超过 {_MAX_READ // 1024 // 1024}MB，只读了前一部分")
    return "\n".join(lines)


def extract_strings(path: str, min_len: int = 4, keyword: str = "", limit: int = 200) -> str:
    """抽 ASCII / UTF-16LE / 中文可打印字符串，带偏移。"""
    min_len = max(1, int(min_len))
    limit = max(1, int(limit))
    data, truncated = _read(path)

    found = []
    for match in re.finditer(rb"[\x20-\x7e]{%d,}" % min_len, data):
        found.append((match.start(), match.group().decode("ascii", "replace")))
    for match in re.finditer(rb"(?:[\x20-\x7e]\x00){%d,}" % min_len, data):
        found.append((match.start(), match.group().decode("utf-16-le", "replace")))
    text = data.decode("utf-8", errors="ignore")
    for match in re.finditer(r"[\u4e00-\u9fff]{2,}", text):
        found.append((match.start(), match.group()))

    if keyword:
        needle = keyword.lower()
        found = [item for item in found if needle in item[1].lower()]

    found.sort()
    lines = [f"文件：{path}"]
    if keyword:
        lines.append(f"含关键字「{keyword}」的字符串：{len(found)} 条")
    else:
        lines.append(f"共提取到 {len(found)} 条可打印字符串（最短 {min_len} 字符）")
    for offset, value in found[:limit]:
        lines.append(f"[0x{offset:08x}] {value}")
    if len(found) > limit:
        lines.append(f"…… 还有 {len(found) - limit} 条没显示，可以加 keyword 过滤或调大 limit")
    if truncated:
        lines.append(f"注意：文件超过 {_MAX_READ // 1024 // 1024}MB，只搜了前一部分")
    return "\n".join(lines)


def carve_files(path: str, out_dir: str = "carved", max_files: int = 50) -> str:
    """按文件头尾签名雕复出内嵌文件，写到 workspace 下的 out_dir。"""
    max_files = max(1, int(max_files))
    data, truncated = _read(path)

    target = safe_path(out_dir)
    os.makedirs(target, exist_ok=True)

    hits = []
    for ext, head, tail in _CARVE_SIGNATURES:
        start = 0
        while True:
            begin = data.find(head, start)
            if begin < 0:
                break
            start = begin + 1
            if tail:
                stop = data.find(tail, begin + len(head))
                if stop < 0:
                    continue
                stop += len(tail)
            else:
                stop = min(begin + _MAX_CARVE_SIZE, len(data))
            hits.append((begin, stop, ext))

    hits.sort()
    lines = [f"样本：{path}", f"命中签名：{len(hits)} 处，写入 workspace/{out_dir}/"]
    written = 0
    for begin, stop, ext in hits:
        if written >= max_files:
            lines.append(f"已达上限 {max_files} 个，剩下的没再写")
            break
        name = f"carved_{written:02d}_{begin:08x}.{ext}"
        with open(os.path.join(target, name), "wb") as f:
            f.write(data[begin:stop])
        lines.append(f"  {name}  偏移 0x{begin:08x}  大小 {stop - begin} 字节")
        written += 1
    if not written:
        lines.append("  没抠出东西：这个样本里没有认识的签名，或者内容被加密 / 压缩过")
    if truncated:
        lines.append(f"注意：文件超过 {_MAX_READ // 1024 // 1024}MB，只扫了前一部分")
    return "\n".join(lines)


def _read_ifd(blob, offset, endian):
    """读一个 EXIF IFD，返回 {tag: (类型, 个数, 原始字节)}。"""
    if offset <= 0 or offset + 2 > len(blob):
        return {}
    total = struct.unpack(endian + "H", blob[offset:offset + 2])[0]
    unit = {1: 1, 2: 1, 3: 2, 4: 4, 5: 8, 7: 1, 9: 4, 10: 8}
    entries = {}
    for index in range(total):
        pos = offset + 2 + index * 12
        if pos + 12 > len(blob):
            break
        tag, ftype, count = struct.unpack(endian + "HHI", blob[pos:pos + 8])
        size = unit.get(ftype, 1) * count
        if size <= 4:
            raw = blob[pos + 8:pos + 8 + size]
        else:
            pointer = struct.unpack(endian + "I", blob[pos + 8:pos + 12])[0]
            raw = blob[pointer:pointer + size]
        entries[tag] = (ftype, count, raw)
    return entries


def _exif_value(entry, endian):
    """把 EXIF 条目转成能读的值。"""
    ftype, count, raw = entry
    try:
        if ftype == 2:
            return raw.split(b"\x00")[0].decode("ascii", "replace").strip()
        if ftype == 3 and len(raw) >= 2:
            return struct.unpack(endian + "H", raw[:2])[0]
        if ftype == 4 and len(raw) >= 4:
            return struct.unpack(endian + "I", raw[:4])[0]
        if ftype in (5, 10) and len(raw) >= 8 * count:
            values = []
            for i in range(count):
                num, den = struct.unpack(endian + "II", raw[i * 8:i * 8 + 8])
                values.append(num / den if den else 0.0)
            return values
    except struct.error:
        return None
    return None


def _jpeg_exif(data):
    """从 JPEG 的 APP1 段里取出 EXIF（TIFF 头开始的那一段）。"""
    if not data.startswith(b"\xff\xd8"):
        return None
    pos = 2
    while pos + 4 <= len(data):
        if data[pos] != 0xFF:
            return None
        marker = data[pos + 1]
        if marker in (0xD8, 0x01) or 0xD0 <= marker <= 0xD7:
            pos += 2
            continue
        if marker == 0xDA:
            return None
        length = struct.unpack(">H", data[pos + 2:pos + 4])[0]
        segment = data[pos + 4:pos + 2 + length]
        if marker == 0xE1 and segment.startswith(b"Exif\x00\x00"):
            return segment[6:]
        pos += 2 + length
    return None


def _exif_report(blob):
    """解析 TIFF 头 + IFD0 + GPS IFD。"""
    if len(blob) < 8:
        return []
    if blob[:2] == b"II":
        endian = "<"
    elif blob[:2] == b"MM":
        endian = ">"
    else:
        return []
    ifd0_offset = struct.unpack(endian + "I", blob[4:8])[0]
    ifd0 = _read_ifd(blob, ifd0_offset, endian)

    lines = []
    for tag, name in _EXIF_IFD0.items():
        if tag in ifd0:
            value = _exif_value(ifd0[tag], endian)
            if value not in (None, ""):
                lines.append(f"EXIF {name}：{value}")

    gps_pointer = ifd0.get(0x8825)
    if gps_pointer:
        gps_offset = struct.unpack(endian + "I", gps_pointer[2][:4])[0] if len(gps_pointer[2]) >= 4 else 0
        gps = _read_ifd(blob, gps_offset, endian)
        values = {}
        for tag in (1, 2, 3, 4, 6):
            if tag in gps:
                values[tag] = _exif_value(gps[tag], endian)
        for ref_tag, deg_tag, label in ((1, 2, "纬度"), (3, 4, "经度")):
            degrees = values.get(deg_tag)
            if isinstance(degrees, list) and len(degrees) >= 3:
                decimal = degrees[0] + degrees[1] / 60 + degrees[2] / 3600
                ref = values.get(ref_tag)
                if ref in ("S", "W"):
                    decimal = -decimal
                lines.append(f"EXIF GPS {label}：{decimal:.6f}（ref={ref}）")
        if isinstance(values.get(6), list) and values[6]:
            lines.append(f"EXIF GPS 海拔：{values[6][0]:.1f} 米")
    return lines


def _time(value):
    return datetime.datetime.fromtimestamp(value).strftime("%Y-%m-%d %H:%M:%S")


def file_metadata(path: str) -> str:
    """MACB 时间戳 + PDF / JPEG 文档元数据。"""
    full = safe_path(path)
    if not os.path.isfile(full):
        return f"错误：文件不存在 {path}"

    stat = os.stat(full)
    lines = [
        f"文件：{path}",
        f"大小：{stat.st_size} 字节",
        f"创建时间：{_time(stat.st_ctime)}",
        f"修改时间：{_time(stat.st_mtime)}",
        f"访问时间：{_time(stat.st_atime)}",
    ]

    head = ""
    with open(full, "rb") as f:
        head = f.read(4096)

    if head.startswith(b"%PDF"):
        try:
            from pypdf import PdfReader

            meta = PdfReader(full).metadata or {}
            for key in ("/Title", "/Author", "/Subject", "/Creator", "/Producer",
                        "/CreationDate", "/ModDate"):
                value = meta.get(key)
                if value:
                    lines.append(f"PDF {key.lstrip('/')}：{value}")
        except Exception as exc:
            lines.append(f"PDF 元数据读取失败：{exc}")
    elif head.startswith(b"\xff\xd8\xff"):
        data, _ = _read(path)
        blob = _jpeg_exif(data)
        lines.extend(_exif_report(blob) if blob else ["没找到 EXIF 段，可能被处理软件抹掉了"])
    else:
        lines.append("这种格式暂无元数据解析（目前支持 PDF 和 JPEG）")

    return "\n".join(lines)
