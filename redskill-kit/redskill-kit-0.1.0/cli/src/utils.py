"""通用工具:错误退出、日志、安全解压、sha256、identifier 校验、渲染辅助。

不依赖任何业务模块。所有上层模块均可直接引用。
"""
from __future__ import annotations

import hashlib
import os
import re
import sys
import zipfile
from pathlib import Path

# ─────────────────────────────────────────
# 版本比较
# ─────────────────────────────────────────
class VersionParseError(ValueError):
    pass


def parse_version(v: str) -> tuple:
    s = (v or "").strip().lstrip("vV")
    if not s:
        raise VersionParseError(f"版本号为空: {v!r}")
    core = s.split("-", 1)[0].split("+", 1)[0]
    parts = []
    for seg in core.split("."):
        if not seg.isdigit():
            raise VersionParseError(f"版本号包含非数字段: {v!r} (段 {seg!r})")
        parts.append(int(seg))
    if not parts:
        raise VersionParseError(f"版本号无可解析数字段: {v!r}")
    return tuple(parts)


def is_newer(candidate: str, current: str) -> bool:
    return parse_version(candidate) > parse_version(current)


# ─────────────────────────────────────────
# 标识符白名单
# ─────────────────────────────────────────
IDENTIFIER_PATTERN = re.compile(r"^[a-zA-Z0-9_-]{1,64}$")


def validate_identifier(identifier: str) -> str:
    if not IDENTIFIER_PATTERN.match(identifier or ""):
        raise ValueError(
            f"identifier 格式不合法: {identifier!r}\n"
            f"       只允许 a-z A-Z 0-9 _ - 共 1-64 字符"
        )
    return identifier


# ─────────────────────────────────────────
# 错误退出 / 日志 / 交互确认
# ─────────────────────────────────────────
def die(msg: str, code: int = 1) -> "NoReturn":  # type: ignore[name-defined]
    print(f"Error: {msg}", file=sys.stderr)
    sys.exit(code)


def confirm_action(prompt: str, yes: bool, non_interactive_hint: str = "非交互模式请加 --yes") -> bool:
    if yes:
        return True
    if sys.stdin.isatty():
        ans = input(prompt).strip().lower()
        if ans != "y":
            print("已取消")
            return False
        return True
    print(f"Error: {non_interactive_hint}", file=sys.stderr)
    raise SystemExit(1)


def verbose_log(msg: str) -> None:
    if os.environ.get("REDSKILL_LOG", "").upper() == "VERBOSE":
        print(f"[redskill][verbose] {msg}", file=sys.stderr)


# ─────────────────────────────────────────
# sha256
# ─────────────────────────────────────────
def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while True:
            chunk = f.read(64 * 1024)
            if not chunk:
                break
            h.update(chunk)
    return h.hexdigest()


def verify_sha256_bytes(data: bytes, expected: str) -> None:
    actual = sha256_bytes(data)
    if actual.lower() != expected.lower():
        raise RuntimeError(
            f"sha256 校验失败: 实际={actual} 期望={expected}"
        )


def verify_sha256_file(path: Path, expected: str) -> None:
    actual = sha256_file(path)
    if actual.lower() != expected.lower():
        raise RuntimeError(
            f"sha256 校验失败: 实际={actual} 期望={expected} 文件={path}"
        )


# ─────────────────────────────────────────
# 安全解压(防 zip-slip + zip bomb)
# ─────────────────────────────────────────
S_IFMT_MASK = 0o170000
S_IFREG = 0o100000
S_IFDIR = 0o040000
S_IFLNK = 0o120000
MAX_ZIP_MEMBERS = 10000
DEFAULT_MAX_EXTRACTED_BYTES = 300 * 1024 * 1024


def _resolve_extract_limit() -> int:
    raw = os.environ.get("REDSKILL_MAX_EXTRACTED_MB", "").strip()
    if raw and raw.isdigit():
        return int(raw) * 1024 * 1024
    return DEFAULT_MAX_EXTRACTED_BYTES


def safe_extract_zip(zip_path: Path, target_dir: Path) -> None:
    """安全解压:只允许目录和普通文件,逐条手动写出,并限制解压后总大小。"""
    target_dir = target_dir.resolve()
    target_dir.mkdir(parents=True, exist_ok=True)

    with zipfile.ZipFile(zip_path, "r") as zf:
        members = zf.infolist()
        if len(members) > MAX_ZIP_MEMBERS:
            raise RuntimeError(f"zip 条目过多: {len(members)} > {MAX_ZIP_MEMBERS}")

        total_uncompressed = 0
        extract_limit = _resolve_extract_limit()

        for member in members:
            name = member.filename

            # 1. 拒绝绝对路径(含 Windows 盘符)
            if name.startswith("/") or name.startswith("\\") or (
                len(name) > 1 and name[1] == ":"
            ):
                raise RuntimeError(f"不安全的 zip 条目(绝对路径): {name}")

            # 2. 拒绝路径穿越
            parts = Path(name).parts
            if ".." in parts:
                raise RuntimeError(f"不安全的 zip 条目(路径穿越): {name}")

            # 3. 计算最终路径并校验仍在 target_dir 之下
            dest = (target_dir / name).resolve()
            try:
                dest.relative_to(target_dir)
            except ValueError:
                raise RuntimeError(f"不安全的 zip 条目(目标越界): {name}")

            # 4. 文件类型白名单(仅 Unix 创建的 zip 才检查 mode)
            if member.create_system == 3:
                mode = (member.external_attr >> 16) & S_IFMT_MASK
                if mode == S_IFLNK:
                    raise RuntimeError(f"不安全的 zip 条目(软链接): {name}")
                if mode != 0 and mode not in (S_IFREG, S_IFDIR):
                    raise RuntimeError(f"不安全的 zip 条目(非常规文件类型): {name}")

            # 5. 目录条目(以 / 结尾)
            if name.endswith("/"):
                dest.mkdir(parents=True, exist_ok=True)
                continue

            total_uncompressed += member.file_size
            if total_uncompressed > extract_limit:
                raise RuntimeError(
                    f"zip 解压后大小超过上限 "
                    f"({total_uncompressed / 1024 / 1024:.1f} MB > {extract_limit / 1024 / 1024:.0f} MB)\n"
                    f"       如确需安装更大包,设置 REDSKILL_MAX_EXTRACTED_MB=<MB> 后重试。"
                )

            # 6. 普通文件:手动写出,不调 zf.extractall
            dest.parent.mkdir(parents=True, exist_ok=True)
            with zf.open(member, "r") as src, open(dest, "wb") as out:
                while True:
                    chunk = src.read(64 * 1024)
                    if not chunk:
                        break
                    out.write(chunk)

            # 7. 恢复可执行位(白名单 mode & 0o755)
            if member.create_system == 3:
                perm = (member.external_attr >> 16) & 0o777
                if perm:
                    os.chmod(dest, perm & 0o755)


# ─────────────────────────────────────────
# 渲染辅助
# ─────────────────────────────────────────
def render_search(payload: dict) -> None:
    """按 API.md §API-2 渲染搜索结果。"""
    results = payload.get("results") or []
    total = payload.get("total", len(results))
    page = payload.get("page", 1)
    limit = payload.get("limit", len(results) or 1)
    if not results:
        print("未找到匹配的 skill")
        return
    pages = max(1, (int(total) + int(limit) - 1) // int(limit)) if limit else 1
    print(f"Found {total} skills (page {page}/{pages}):\n")
    for item in results:
        # 兼容服务端用 slug 字段(API.md 规范字段为 identifier,实际后端可能用 slug)
        ident = item.get("identifier") or item.get("slug") or "?"
        name = item.get("name") or item.get("displayName") or ""
        desc = item.get("description") or ""
        version = item.get("version") or ""
        tags = item.get("tags") or []
        author = item.get("author") or ""
        print(f"{ident}  {name}".rstrip())
        if desc:
            print(f"  - {desc}")
        meta_bits = []
        if version:
            meta_bits.append(f"version: {version}")
        if tags:
            meta_bits.append("tags: " + ", ".join(tags))
        if author:
            meta_bits.append(f"author: {author}")
        if meta_bits:
            print("  - " + "  ".join(meta_bits))
        print()
    print('You can use "redskill install <identifier>" to install.')


def render_list(entries: list) -> None:
    if not entries:
        print("(尚未安装任何 skill)")
        return
    for e in entries:
        broken = " [broken]" if e.get("broken") else ""
        ver = e.get("version") or ""
        name = e.get("name") or e.get("identifier")
        install_dir = e.get("install_dir") or ""
        print(f"{e['identifier']}  {name}  {ver}{broken}")
        if install_dir:
            print(f"  → {install_dir}")
