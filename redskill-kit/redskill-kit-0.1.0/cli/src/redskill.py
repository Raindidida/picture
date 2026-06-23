#!/usr/bin/env python3
"""redskill CLI 入口"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from config import load_metadata, load_version  # noqa: E402
from api import UrlNotConfiguredError  # noqa: E402
from utils import validate_identifier, render_search, render_list  # noqa: E402
import installer  # noqa: E402
import lockfile  # noqa: E402
import self_upgrade  # noqa: E402
import api  # noqa: E402


def cmd_install(args):
    validate_identifier(args.identifier)
    metadata = load_metadata()
    install_root = Path(args.dir).resolve()
    installer.install_skill(args.identifier, install_root, args.force, metadata)


def cmd_search(args):
    metadata = load_metadata()
    payload = api.search(" ".join(args.query), args.limit, metadata)
    render_search(payload)


def cmd_list(args):
    install_root = Path(args.dir).resolve()
    entries = lockfile.list_entries(install_root=install_root)
    render_list(entries)


def cmd_uninstall(args):
    validate_identifier(args.identifier)
    install_root = Path(args.dir).resolve()
    installer.uninstall_skill(args.identifier, install_root)


def cmd_upgrade(args):
    validate_identifier(args.identifier)
    metadata = load_metadata()
    install_root = Path(args.dir).resolve()
    installer.upgrade_skill(args.identifier, install_root, args.yes, metadata)


def cmd_self_upgrade(args):
    metadata = load_metadata()
    return self_upgrade.run_self_upgrade(metadata, args.check_only, args.yes)


def build_parser():
    p = argparse.ArgumentParser(prog="redskill")
    p.add_argument("-v", "--version", action="version",
                   version=f"redskill {load_version()}")
    sub = p.add_subparsers(dest="command", required=True)

    install = sub.add_parser("install", help="安装 skill")
    install.add_argument("identifier")
    install.add_argument("--dir", default="./skills",
                         help="安装根目录 (默认: ./skills)")
    install.add_argument("--force", action="store_true")
    install.set_defaults(func=cmd_install)

    search = sub.add_parser("search", help="搜索 skill")
    search.add_argument("query", nargs="+")
    search.add_argument("--limit", type=int, default=20)
    search.set_defaults(func=cmd_search)

    list_cmd = sub.add_parser("list", help="列出安装根目录下已装 skill")
    list_cmd.add_argument("--dir", default="./skills",
                          help="安装根目录 (默认: ./skills)")
    list_cmd.set_defaults(func=cmd_list)

    uninstall = sub.add_parser("uninstall", help="卸载 skill")
    uninstall.add_argument("identifier")
    uninstall.add_argument("--dir", default="./skills",
                           help="安装根目录 (默认: ./skills)")
    uninstall.set_defaults(func=cmd_uninstall)

    upgrade = sub.add_parser("upgrade", help="升级已安装的 skill")
    upgrade.add_argument("identifier")
    upgrade.add_argument("--dir", default="./skills",
                         help="安装根目录 (默认: ./skills)")
    upgrade.add_argument("--yes", "-y", action="store_true", help="非交互模式")
    upgrade.set_defaults(func=cmd_upgrade)

    self_upg = sub.add_parser("self-upgrade", help="升级 CLI 本身")
    self_upg.add_argument("--check-only", action="store_true",
                          help="只检查不升级 (有更新 exit 10,无更新 exit 0)")
    self_upg.add_argument("--yes", "-y", action="store_true",
                          help="非交互模式,自动确认")
    self_upg.set_defaults(func=cmd_self_upgrade)

    return p


def main():
    parser = build_parser()
    args = parser.parse_args()
    try:
        rc = args.func(args)
        sys.exit(rc or 0)
    except UrlNotConfiguredError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(2)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(3)
    except KeyboardInterrupt:
        print("\n已取消", file=sys.stderr)
        sys.exit(130)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
