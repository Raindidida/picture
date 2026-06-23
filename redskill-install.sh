#!/usr/bin/env bash
# RedSkill 安装器
#
# 用法:
#   curl -fsSL <安装脚本 URL> | bash
#   curl -fsSL <安装脚本 URL> | bash -s -- --cli-only
set -euo pipefail

DOWNLOAD_URL="${REDSKILL_KIT_URL:-https://fe-video-qc.xhscdn.com/fe-platform-file/104101b8320fbj1oq6e0653u0hejenq0004pf88g3n4mm4.gz}"

need_cmd() {
  command -v "$1" >/dev/null 2>&1 || {
    echo "Error: 缺少命令 '$1', 请先安装" >&2
    exit 1
  }
}
need_cmd curl
need_cmd tar

printf '== RedSkill 安装器 ==\n'

TMP_DIR="$(mktemp -d 2>/dev/null || mktemp -d -t redskill-bootstrap)"
trap 'rm -rf "${TMP_DIR}"' EXIT

TARBALL="${TMP_DIR}/kit.tar.gz"

printf '   下载中...\n'
if ! curl -fsSL "${DOWNLOAD_URL}" -o "${TARBALL}"; then
  echo "Error: 下载失败" >&2
  exit 1
fi

printf '   解压中...\n'
EXTRACT_DIR="${TMP_DIR}/extracted"
mkdir -p "${EXTRACT_DIR}"
if ! tar -xzf "${TARBALL}" -C "${EXTRACT_DIR}"; then
  echo "Error: 安装包解压失败" >&2
  exit 1
fi

INSTALLER="$(find "${EXTRACT_DIR}" -mindepth 1 -maxdepth 4 -type f -name install.sh 2>/dev/null | head -n 1)"
if [[ -z "${INSTALLER}" || ! -f "${INSTALLER}" ]]; then
  echo "Error: 安装包内容异常" >&2
  exit 1
fi

exec bash "${INSTALLER}" "$@"
