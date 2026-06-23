"""RedSkill lockfile 读写、进程级文件锁、原子写入。

不直接操作文件系统(rmtree 等),目录交换收敛在 installer 模块,
本模块只负责 JSON 状态。
"""
from __future__ import annotations

import json
import os
import time
from contextlib import contextmanager
from pathlib import Path

try:
    import fcntl
except ImportError:
    fcntl = None

LOCK_PATH = Path("~/.redskill/lock.json").expanduser()
LOCK_GUARD_PATH = Path("~/.redskill/lock.json.guard").expanduser()
LOCKFILE_NAME = ".redskill-lock.json"


@contextmanager
def exclusive_lock():
    """同一用户下 install/uninstall 的进程级互斥锁(macOS / Linux)。

    必须把目录交换和 lockfile 写入都放在同一个 with 块里,
    否则单次 JSON 原子写无法保护跨步骤事务。
    """
    LOCK_GUARD_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(LOCK_GUARD_PATH, "a+", encoding="utf-8") as fp:
        if fcntl is None:
            yield
            return
        fcntl.flock(fp.fileno(), fcntl.LOCK_EX)
        try:
            yield
        finally:
            fcntl.flock(fp.fileno(), fcntl.LOCK_UN)


def _lock_path(install_root: Path = None) -> Path:
    if install_root is None:
        return LOCK_PATH
    return Path(install_root).expanduser().resolve() / LOCKFILE_NAME


def load_lock(install_root: Path = None) -> dict:
    path = _lock_path(install_root)
    if not path.exists():
        return {"version": 1, "skills": {}}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {"version": 1, "skills": {}}
    if not isinstance(data, dict) or "skills" not in data or not isinstance(data.get("skills"), dict):
        return {"version": 1, "skills": {}}
    return data


def save_lock(lock: dict, install_root: Path = None) -> None:
    """原子写入:同目录临时文件 + os.replace。"""
    path = _lock_path(install_root)
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(f".lock.{os.getpid()}.tmp")
    tmp.write_text(json.dumps(lock, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    os.replace(str(tmp), str(path))


def add_entry(identifier: str, bundle, install_dir: Path, install_root: Path = None) -> None:
    lock_root = Path(install_root).expanduser().resolve() if install_root is not None else None
    lock = load_lock(lock_root)
    lock["skills"][identifier] = {
        "name": getattr(bundle, "name", None) or identifier,
        "version": getattr(bundle, "version", None) or "",
        "source": getattr(bundle, "source", "redskill"),
        "install_dir": str(install_dir),
        "installed_at": str(int(time.time() * 1000)),
        "sha256": getattr(bundle, "sha256", None) or "",
    }
    save_lock(lock, lock_root)


def remove_entry_only(identifier: str, install_root: Path = None) -> None:
    """仅从 lockfile 移除 entry,不动文件系统。"""
    lock_root = Path(install_root).expanduser().resolve() if install_root is not None else None
    lock = load_lock(lock_root)
    if identifier in lock.get("skills", {}):
        del lock["skills"][identifier]
        save_lock(lock, lock_root)


def list_entries(filter_dir: Path = None, install_root: Path = None) -> list:
    """返回 entry 列表,每项含 broken 标记。"""
    lock = load_lock(install_root)
    out = []
    for ident, meta in sorted(lock.get("skills", {}).items()):
        install_dir = Path(meta.get("install_dir", "")).expanduser()
        if filter_dir is not None and not _is_under(install_dir, filter_dir):
            continue
        broken = not install_dir.exists()
        out.append({"identifier": ident, "broken": broken, **meta})
    return out


def _is_under(path: Path, root: Path) -> bool:
    try:
        path.resolve().relative_to(root.resolve())
        return True
    except (ValueError, OSError):
        return False
