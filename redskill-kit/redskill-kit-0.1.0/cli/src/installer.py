"""skill 安装/卸载:stage/backup 同分区交换、安全守卫、lockfile 事务。

只通过 api.* 调外部接口,只调 lockfile.add_entry/remove_entry_only,
所有 rmtree 都收敛在本模块,统一受 _assert_safe_target 保护。
"""
from __future__ import annotations

import json
import os
import shutil
import tempfile
import time
from pathlib import Path

import api
import lockfile
import utils

SYSTEM_ROOTS = {
    Path("/"), Path("/usr"), Path("/etc"), Path("/var"),
    Path("/home"), Path("/Users"), Path("/opt"), Path("/private"),
    Path.home(),
}

INSTALL_MARK_NAME = ".redskill-installed"
INSTALL_MARK_VERSION = 1


def _process_uid() -> int:
    getuid = getattr(os, "getuid", None)
    return getuid() if getuid else 0


# ─────────────────────────────────────────
# 安全守卫
# ─────────────────────────────────────────
def _assert_safe_target(target_dir: Path, install_root: Path, identifier: str) -> None:
    """四重守卫:防止误删根目录或用户家目录。

    target_dir / install_root 都必须是 .resolve() 后的绝对路径。
    """
    # 1. target 必须严格在 install_root 之下,且只多一段 == identifier
    try:
        rel = target_dir.relative_to(install_root)
    except ValueError:
        raise RuntimeError(f"目标越界: {target_dir} 不在 {install_root} 之下")
    if rel.parts != (identifier,):
        raise RuntimeError(f"目标路径异常: {target_dir} (期望 {install_root}/{identifier})")

    # 2. install_root 不能是文件系统根
    if install_root == install_root.parent:
        raise RuntimeError(f"install_root 是文件系统根,拒绝执行: {install_root}")

    # 3. install_root 自身和 target 自身均不能命中黑名单
    if install_root in SYSTEM_ROOTS:
        raise RuntimeError(f"install_root 命中黑名单,拒绝执行: {install_root}")
    if target_dir in SYSTEM_ROOTS:
        raise RuntimeError(f"target_dir 命中黑名单,拒绝执行: {target_dir}")

    # 4. install_root 父级不能是系统根(避免根级单目录被当成 install_root)
    if install_root.parent in SYSTEM_ROOTS:
        raise RuntimeError(
            f"install_root 父级是系统根 ({install_root.parent}),"
            f"拒绝在根级单目录下安装: {install_root}"
        )


def assert_safe_to_remove(target_dir: Path, identifier: str,
                          expect_filter_dir: Path = None) -> None:
    """uninstall 专用:基于 lockfile 删除前必须通过的守卫。"""
    target_dir = target_dir.resolve()

    install_root = target_dir.parent
    _assert_safe_target(target_dir, install_root, identifier)

    if expect_filter_dir is not None:
        expect_filter_dir = expect_filter_dir.resolve()
        try:
            install_root.relative_to(expect_filter_dir)
        except ValueError:
            raise RuntimeError(
                f"{identifier} 的安装目录 {install_root} 不在 --dir {expect_filter_dir} 之下,拒绝删除"
            )

    mark = target_dir / INSTALL_MARK_NAME
    if not mark.exists():
        raise RuntimeError(
            f"目标目录缺少安装标记: {mark}\n"
            f"       该目录可能并非由 redskill install 创建,拒绝删除。\n"
            f"       如确认要删,请手动 rm -rf {target_dir} 后再 redskill uninstall {identifier}。"
        )
    try:
        meta = json.loads(mark.read_text(encoding="utf-8"))
    except Exception as e:
        raise RuntimeError(f"安装标记无法解析: {mark} ({e})")
    if meta.get("identifier") != identifier:
        raise RuntimeError(
            f"安装标记 identifier 不匹配: 标记={meta.get('identifier')!r} 期望={identifier!r}\n"
            f"       拒绝删除 {target_dir}。"
        )


def _write_install_mark(target_dir: Path, identifier: str, bundle) -> None:
    payload = {
        "mark_version": INSTALL_MARK_VERSION,
        "identifier": identifier,
        "version": getattr(bundle, "version", None) or "",
        "sha256": getattr(bundle, "sha256", None) or "",
        "installed_at": str(int(time.time() * 1000)),
    }
    (target_dir / INSTALL_MARK_NAME).write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


# ─────────────────────────────────────────
# install 主流程
# ─────────────────────────────────────────
def install_skill(identifier: str, install_root: Path, force: bool, metadata: dict,
                  bundle_result=None) -> None:
    install_root = install_root.resolve()
    try:
        install_root.mkdir(parents=True, exist_ok=True)
    except PermissionError as e:
        raise RuntimeError(
            f"无权限创建安装根目录 {install_root}: {e}\n"
            f"       请换一个可写目录(如 ~/skills),或用 sudo。"
        )
    if not os.access(install_root, os.W_OK):
        raise RuntimeError(
            f"安装根目录不可写: {install_root}\n"
            f"       请换一个可写目录,或用 sudo。"
        )
    target_dir = (install_root / identifier).resolve()
    _assert_safe_target(target_dir, install_root, identifier)

    # 1. 调 api 拉 bundle (或复用预获取的结果)
    if bundle_result is not None:
        result = bundle_result
    else:
        utils.verbose_log(f"GET skill bundle: {identifier}")
        result = api.get_skill_bundle(identifier, metadata)
    zip_bytes = result.zip_bytes if result.zip_bytes else api.download_bytes(result.zip_url)

    if not result.sha256 and os.environ.get("REDSKILL_ALLOW_UNSIGNED_BUNDLE") != "1":
        raise RuntimeError(
            "skill 包缺少 sha256,拒绝安装\n"
            "       生产环境必须由后端返回 X-Skill-Sha256 或 manifest.sha256。\n"
            "       本地联调如需临时跳过,显式设置 REDSKILL_ALLOW_UNSIGNED_BUNDLE=1。"
        )
    if result.sha256:
        utils.verify_sha256_bytes(zip_bytes, result.sha256)

    # 2. 写 zip 到临时文件 + 解压到 stage(同分区)
    pid = os.getpid()
    uid = _process_uid()
    stage = install_root / f".{identifier}.stage.{uid}.{pid}"
    backup = install_root / f".{identifier}.bak.{uid}.{pid}"

    if stage.exists():
        shutil.rmtree(stage)
    stage.mkdir()

    with tempfile.NamedTemporaryFile(
        prefix=f"redskill-{uid}-", suffix=".zip",
        dir=str(install_root), delete=False
    ) as tmp:
        tmp.write(zip_bytes)
        zip_path = Path(tmp.name)

    try:
        utils.safe_extract_zip(zip_path, stage)
    finally:
        try:
            zip_path.unlink()
        except FileNotFoundError:
            pass

    # 3. 在 stage 内预先写入安装标记
    _write_install_mark(stage, identifier, result)

    # 4. 进程锁内交换 + lockfile 事务
    with lockfile.exclusive_lock():
        had_old = target_dir.exists()
        if had_old:
            if not force:
                shutil.rmtree(stage, ignore_errors=True)
                raise RuntimeError(f"目标已存在: {target_dir} (使用 --force 覆盖)")
            os.rename(target_dir, backup)

        try:
            os.rename(stage, target_dir)
        except Exception as e:
            shutil.rmtree(stage, ignore_errors=True)
            if had_old and backup.exists():
                try:
                    os.rename(backup, target_dir)
                except Exception:
                    pass
            raise RuntimeError(f"安装失败已回滚: {e}")

        # 5. 写 lockfile,同事务
        try:
            lockfile.add_entry(identifier, result, target_dir, install_root)
        except Exception as e:
            rollback_errs = []
            try:
                shutil.rmtree(target_dir)
            except Exception as re:
                rollback_errs.append(f"删除新 target 失败: {re}")
            if had_old and backup.exists():
                try:
                    os.rename(backup, target_dir)
                except Exception as re:
                    rollback_errs.append(f"恢复 backup 失败: {re}")
            if rollback_errs:
                raise RuntimeError(
                    f"lockfile 写入失败 ({e}),且回滚未完成:\n  - "
                    + "\n  - ".join(rollback_errs)
                    + f"\n  请手动清理残留目录 {target_dir} 和/或 {backup} 后重试。"
                )
            raise RuntimeError(f"lockfile 写入失败,已回滚目录到旧版本: {e}")

        # 6. 全部成功:清 backup
        if backup.exists():
            shutil.rmtree(backup, ignore_errors=True)

    print(
        f"✓ Installed: {identifier}"
        + (f"@{result.version}" if result.version else "")
        + f" -> {target_dir}"
    )


# ─────────────────────────────────────────
# upgrade 主流程
# ─────────────────────────────────────────
def upgrade_skill(identifier: str, install_root: Path = None,
                  yes: bool = False, metadata: dict = None) -> None:
    install_root = install_root.resolve() if install_root is not None else None
    lock = lockfile.load_lock(install_root)
    entry = lock.get("skills", {}).get(identifier)
    if not entry:
        raise RuntimeError(f"未安装该 skill: {identifier}")

    install_dir = Path(entry["install_dir"]).expanduser().resolve()
    assert_safe_to_remove(install_dir, identifier, expect_filter_dir=install_root)
    current_version = entry.get("version") or ""

    utils.verbose_log(f"checking upgrade: {identifier} current={current_version}")
    result = api.get_skill_bundle(identifier, metadata)
    remote_version = result.version or ""

    try:
        has_update = remote_version and utils.is_newer(remote_version, current_version)
    except utils.VersionParseError:
        has_update = True

    if not has_update:
        print(f"已是最新: {identifier}@{current_version}")
        return

    print(f"发现新版本: {identifier} {current_version} → {remote_version}")
    if not utils.confirm_action("是否升级? [y/N]: ", yes):
        return

    install_skill(identifier, install_dir.parent, force=True, metadata=metadata,
                  bundle_result=result)


# ─────────────────────────────────────────
# uninstall 主流程
# ─────────────────────────────────────────
def uninstall_skill(identifier: str, install_root: Path = None) -> None:
    """卸载:目录删除和 lockfile 删除同事务,失败时恢复目录。"""
    install_root = install_root.resolve() if install_root is not None else None
    with lockfile.exclusive_lock():
        lock = lockfile.load_lock(install_root)
        entry = lock.get("skills", {}).get(identifier)
        if not entry:
            raise RuntimeError(f"未安装该 skill: {identifier}")

        install_dir = Path(entry["install_dir"]).expanduser().resolve()
        assert_safe_to_remove(install_dir, identifier, expect_filter_dir=install_root)

        pid = os.getpid()
        uid = _process_uid()
        backup = install_dir.parent / f".{identifier}.uninstall.{uid}.{pid}"
        if backup.exists():
            shutil.rmtree(backup)

        # 1. rename 到同分区 backup
        os.rename(install_dir, backup)

        # 2. 删 lockfile entry
        try:
            lockfile.remove_entry_only(identifier, install_root)
        except Exception as e:
            rollback_errs = []
            if backup.exists() and not install_dir.exists():
                try:
                    os.rename(backup, install_dir)
                except Exception as re:
                    rollback_errs.append(f"恢复目录失败: {re}")
            else:
                rollback_errs.append(
                    f"backup 异常: backup_exists={backup.exists()} install_dir_exists={install_dir.exists()}"
                )
            if rollback_errs:
                raise RuntimeError(
                    f"卸载 lockfile 写入失败 ({e}),且回滚未完成:\n  - "
                    + "\n  - ".join(rollback_errs)
                    + f"\n  请手动检查 {install_dir} 与 {backup}。"
                )
            raise RuntimeError(f"卸载失败已回滚目录: {e}")

        # 3. 真正删除 backup
        shutil.rmtree(backup, ignore_errors=True)

    print(f"✓ Uninstalled: {identifier}")
