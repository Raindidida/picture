"""CLI 自升级:OTA 事务流程。

manifest sha256 强制必填,事务替换 src/ + version.json,任一失败完整回滚。
"""
from __future__ import annotations

import json
import os
import shutil
import sys
from pathlib import Path

import api
import config
import utils
from utils import is_newer as _is_newer, VersionParseError


def _remove_path(path: Path) -> None:
    if not path.exists() and not path.is_symlink():
        return
    if path.is_dir() and not path.is_symlink():
        shutil.rmtree(path, ignore_errors=True)
    else:
        try:
            path.unlink()
        except FileNotFoundError:
            pass


def _same_filesystem(p1: Path, p2: Path) -> bool:
    def first_existing(p: Path):
        for cand in (p, *p.parents):
            if cand.exists():
                return cand
        return None
    a = first_existing(p1)
    b = first_existing(p2)
    if a is None or b is None:
        return False
    return os.stat(a).st_dev == os.stat(b).st_dev


def _atomic_swap_release(home: Path, stage: Path, items: list) -> None:
    """同事务替换多个文件/目录,任一失败完整回滚。"""
    if not _same_filesystem(home, stage):
        raise RuntimeError(
            f"自升级 stage ({stage}) 与 home ({home}) 跨分区,"
            f"无法保证原子替换。请检查 ~/.redskill 是否被 symlink 到其他分区。"
        )

    pid = os.getpid()
    uid = os.getuid()
    backup = home / f".bak.{uid}.{pid}"
    backup.mkdir(parents=True, exist_ok=True)

    moved_to_backup = []
    moved_to_home = []

    try:
        for item in items:
            cur = home / item
            if cur.exists() or cur.is_symlink():
                bak = backup / item
                bak.parent.mkdir(parents=True, exist_ok=True)
                os.rename(cur, bak)
                moved_to_backup.append((item, bak))

        for item in items:
            src = stage / item
            if not src.exists():
                raise RuntimeError(f"升级包缺少: {item}")
            os.rename(src, home / item)
            moved_to_home.append(item)

        _remove_path(backup)

    except Exception as e:
        rollback_errs = []
        for item in moved_to_home:
            try:
                _remove_path(home / item)
            except Exception as re:
                rollback_errs.append(f"删除 home/{item} 失败: {re}")
        for item_name, bak_path in moved_to_backup:
            try:
                os.rename(bak_path, home / item_name)
            except Exception as re:
                rollback_errs.append(f"恢复 {item_name} 失败: {re}")
        if rollback_errs:
            raise RuntimeError(
                f"自升级失败 ({e}),且回滚未完成:\n  - "
                + "\n  - ".join(rollback_errs)
                + f"\n  请手动检查 {home} 和 {backup},可能需要从 backup 手动恢复 src/version.json。"
            )
        raise RuntimeError(f"自升级失败已回滚: {e}")


def run_self_upgrade(metadata: dict, check_only: bool, yes: bool) -> int:
    manifest = api.get_cli_manifest(metadata)

    current = config.load_version()
    try:
        if not _is_newer(manifest.version, current):
            print(f"已是最新: {current}")
            return 0
    except VersionParseError as e:
        raise RuntimeError(f"版本号格式非法: {e}")

    print(f"发现新版本: {current} → {manifest.version}")
    if manifest.release_notes:
        print(f"更新说明: {manifest.release_notes}")

    if check_only:
        return 10

    if not yes:
        if not utils.confirm_action("是否升级? [y/N]: ", yes=False,
                                     non_interactive_hint="非交互模式请加 --yes 或 --check-only"):
            return 0
            return 1

    home = config.REDSKILL_HOME
    pid = os.getpid()
    uid = os.getuid()
    workdir = home / f".upgrade.{uid}.{pid}"
    workdir.mkdir(parents=True, exist_ok=True)

    try:
        zip_path = workdir / "bundle.zip"
        zip_path.write_bytes(api.download_bytes(manifest.zip_url))
        if manifest.sha256:
            utils.verify_sha256_file(zip_path, manifest.sha256)
        elif os.environ.get("REDSKILL_ALLOW_UNSIGNED_CLI") != "1":
            raise RuntimeError(
                "CLI 升级包缺少 sha256,拒绝执行\n"
                "       生产环境必须由 manifest 提供 sha256(防 MITM 替换 CLI 代码)。\n"
                "       本地联调如需临时跳过,显式设置 REDSKILL_ALLOW_UNSIGNED_CLI=1。"
            )

        stage = workdir / "stage"
        utils.safe_extract_zip(zip_path, stage)

        # 校验包结构
        if not (stage / "src" / "redskill.py").exists():
            raise RuntimeError("升级包结构异常: 缺少 src/redskill.py")
        if not (stage / "version.json").exists():
            raise RuntimeError("升级包结构异常: 缺少 version.json")
        try:
            pkg_ver = json.loads((stage / "version.json").read_text(encoding="utf-8")).get("version")
        except Exception as e:
            raise RuntimeError(f"升级包 version.json 无法解析: {e}")
        if pkg_ver != manifest.version:
            raise RuntimeError(
                f"升级包版本不一致: manifest={manifest.version} package={pkg_ver}"
            )

        _atomic_swap_release(home, stage, items=["src", "version.json"])
    finally:
        shutil.rmtree(workdir, ignore_errors=True)

    print(f"✓ Self-upgrade complete: {current} → {manifest.version}")
    return 0
