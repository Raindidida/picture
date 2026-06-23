#!/usr/bin/env bash
# RedSkill kit 安装器
#
# 与 Tencent skillhub 风格不同:
#  - 用 --components <逗号分隔列表> 选装,而不是 --cli-only / --plugin-only / --skill-only
#    (单选标志保留为兼容别名,不推荐)
#  - 支持 --dry-run 仅预览不动盘
#  - 输出加 [ok] / [skip] / [warn] / [done] 前缀,单组件状态一目了然
#  - 全部目标路径与默认动作集中在脚本顶部「manifest 区」,改路径无需翻改函数体
set -euo pipefail

# ─────────────────────────────────────
# Manifest:可装组件清单
# ─────────────────────────────────────
ALL_COMPONENTS=(cli skill plugin)
DEFAULT_COMPONENTS="cli,skill"

INSTALL_BASE="${HOME}/.redskill"
BIN_DIR="${HOME}/.local/bin"
OPENCLAW_BASE="${HOME}/.openclaw"

CLI_SRC_TARGET="${INSTALL_BASE}/src"
CLI_VERSION_TARGET="${INSTALL_BASE}/version.json"
CLI_METADATA_TARGET="${INSTALL_BASE}/metadata.json"
CLI_CONFIG_TARGET="${INSTALL_BASE}/config.json"
CLI_WRAPPER_TARGET="${BIN_DIR}/redskill"

PLUGIN_TARGET_DIR="${OPENCLAW_BASE}/extensions/redskill"
SKILL_FIND_TARGET="${OPENCLAW_BASE}/workspace/skills/find-redskills/SKILL.md"
SKILL_PREF_TARGET="${OPENCLAW_BASE}/workspace/skills/redskill-preference/SKILL.md"

# ─────────────────────────────────────
# 命令行解析
# ─────────────────────────────────────
COMPONENTS=""
SKILLS_PREF="default"   # default | on | off
RESET_METADATA=0
DRY_RUN=0
RESTART_GATEWAY=0

usage() {
  cat <<USAGE
Usage: install.sh [选项]

  --components LIST    逗号分隔,从 [${ALL_COMPONENTS[*]}] 中选,例:--components cli,plugin
                       省略时使用默认值: ${DEFAULT_COMPONENTS}
  --cli-only           等价于 --components cli   (兼容别名)
  --plugin-only        等价于 --components plugin
  --skill-only         等价于 --components skill
  --no-skills          跳过 workspace skill,并把偏好写入 ${CLI_CONFIG_TARGET}
  --with-skills        强制启用 workspace skill 并把偏好写入 config
  --reset-metadata     强制覆盖已有 metadata.json(自动备份带时间戳)
  --restart-gateway    安装完拉起 openclaw gateway(若可用)
  --dry-run            仅打印将要做的事,不动盘
  -h, --help           本帮助
USAGE
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --components)
      [[ -n "${2:-}" ]] || { echo "Error: --components 需要参数" >&2; exit 2; }
      COMPONENTS="$2"; shift 2 ;;
    --components=*)         COMPONENTS="${1#*=}"; shift ;;
    --cli-only)             COMPONENTS="cli"; shift ;;
    --plugin-only)          COMPONENTS="plugin"; shift ;;
    --skill-only)           COMPONENTS="skill"; shift ;;
    --no-skills)            SKILLS_PREF="off"; shift ;;
    --with-skills)          SKILLS_PREF="on"; shift ;;
    --reset-metadata)       RESET_METADATA=1; shift ;;
    --restart-gateway)      RESTART_GATEWAY=1; shift ;;
    --dry-run)              DRY_RUN=1; shift ;;
    -h|--help)              usage; exit 0 ;;
    *) echo "Error: unknown argument: $1" >&2; usage; exit 2 ;;
  esac
done

[[ -z "${COMPONENTS}" ]] && COMPONENTS="${DEFAULT_COMPONENTS}"

SELECTED=" "
IFS=',' read -ra _parts <<< "${COMPONENTS}"
for c in "${_parts[@]}"; do
  key="${c// /}"
  [[ -z "${key}" ]] && continue
  case " ${ALL_COMPONENTS[*]} " in
    *" ${key} "*) SELECTED+="${key} " ;;
    *) echo "Error: 未知 component: ${key} (合法值: ${ALL_COMPONENTS[*]})" >&2; exit 2 ;;
  esac
done

# 注意:component 名只允许 [a-z]+,不要塞 glob 元字符(* ? [),否则 [[ == ]] 会按模式匹配
want() { [[ "${SELECTED}" == *" $1 "* ]]; }

if [[ "${SKILLS_PREF}" == "off" ]]; then
  SELECTED="${SELECTED// skill / }"
fi

# ─────────────────────────────────────
# 输出 helpers
# ─────────────────────────────────────
log_ok()   { printf '[ok]   %s\n' "$*"; }
log_skip() { printf '[skip] %s\n' "$*"; }
log_warn() { printf '[warn] %s\n' "$*" >&2; }
log_done() { printf '[done] %s\n' "$*"; }
log_step() { printf '\n[step] %s\n' "$*"; }

run() {
  if [[ "${DRY_RUN}" -eq 1 ]]; then
    printf '       (dry-run) %s\n' "$*"
  else
    "$@"
  fi
}

# ─────────────────────────────────────
# 来源目录
# ─────────────────────────────────────
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CLI_SRC_DIR="${SCRIPT_DIR}/cli"
PLUGIN_SRC_DIR="${SCRIPT_DIR}/plugin"
SKILL_SRC_DIR="${SCRIPT_DIR}/skill"

# ─────────────────────────────────────
# 组件:cli
# ─────────────────────────────────────
component_cli() {
  log_step "组件 cli — Python CLI + wrapper"

  if ! command -v python3 >/dev/null 2>&1; then
    log_warn "python3 未找到,放弃 cli 组件"
    return 1
  fi
  local pyver pymaj pymin
  pyver=$(python3 -c 'import sys; print("%d.%d" % sys.version_info[:2])')
  pymaj=${pyver%.*}; pymin=${pyver#*.}
  if [[ "${pymaj}" -lt 3 || ( "${pymaj}" -eq 3 && "${pymin}" -lt 8 ) ]]; then
    log_warn "需要 Python 3.8+,当前 ${pyver}"
    return 1
  fi
  log_ok "python3 ${pyver} 满足 ≥ 3.8"

  run mkdir -p "${INSTALL_BASE}" "${BIN_DIR}"

  run rm -rf "${CLI_SRC_TARGET}"
  run cp -r "${CLI_SRC_DIR}/src" "${CLI_SRC_TARGET}"
  log_ok "src/ → ${CLI_SRC_TARGET}"

  run cp "${CLI_SRC_DIR}/version.json" "${CLI_VERSION_TARGET}"
  log_ok "version.json → ${CLI_VERSION_TARGET}"

  if [[ -f "${CLI_METADATA_TARGET}" && "${RESET_METADATA}" -eq 0 ]]; then
    log_skip "metadata.json 已存在(用 --reset-metadata 强制覆盖)"
  else
    if [[ -f "${CLI_METADATA_TARGET}" ]]; then
      local ts; ts=$(date +%Y%m%d%H%M%S)
      run cp "${CLI_METADATA_TARGET}" "${CLI_METADATA_TARGET}.bak.${ts}"
      log_ok "已备份旧 metadata.json → metadata.json.bak.${ts}"
    fi
    run cp "${CLI_SRC_DIR}/metadata.json" "${CLI_METADATA_TARGET}"
    log_ok "metadata.json → ${CLI_METADATA_TARGET}"
  fi

  if [[ "${DRY_RUN}" -eq 1 ]]; then
    printf '       (dry-run) write wrapper to %s\n' "${CLI_WRAPPER_TARGET}"
  else
    cat > "${CLI_WRAPPER_TARGET}" <<'WRAPPER'
#!/usr/bin/env bash
exec python3 "${HOME}/.redskill/src/redskill.py" "$@"
WRAPPER
    chmod +x "${CLI_WRAPPER_TARGET}"
  fi
  log_ok "wrapper → ${CLI_WRAPPER_TARGET}"

  case ":${PATH}:" in
    *":${BIN_DIR}:"*) ;;
    *) log_warn "${BIN_DIR} 不在 PATH 中,加一行: export PATH=\"${BIN_DIR}:\$PATH\"" ;;
  esac
}

# ─────────────────────────────────────
# 组件:skill
# ─────────────────────────────────────
component_skill() {
  log_step "组件 skill — workspace SKILL.md(find-redskills + redskill-preference)"

  local find_src="${SKILL_SRC_DIR}/SKILL.md"
  local pref_src="${SKILL_SRC_DIR}/SKILL.redskill-preference.md"
  local installed=0

  if [[ -f "${find_src}" ]]; then
    run mkdir -p "$(dirname "${SKILL_FIND_TARGET}")"
    run cp "${find_src}" "${SKILL_FIND_TARGET}"
    log_ok "find-redskills → ${SKILL_FIND_TARGET}"
    installed=1
  else
    log_warn "缺源文件: ${find_src}"
  fi

  if [[ -f "${pref_src}" ]]; then
    run mkdir -p "$(dirname "${SKILL_PREF_TARGET}")"
    run cp "${pref_src}" "${SKILL_PREF_TARGET}"
    log_ok "redskill-preference → ${SKILL_PREF_TARGET}"
    installed=1
  else
    log_warn "缺源文件: ${pref_src}"
  fi

  if [[ "${installed}" -ne 1 ]]; then
    log_warn "skill 组件无任何模板被安装"
  fi
}

# ─────────────────────────────────────
# 组件:plugin
# ─────────────────────────────────────
component_plugin() {
  log_step "组件 plugin — openclaw 插件"

  if [[ ! -d "${PLUGIN_SRC_DIR}" ]]; then
    log_warn "kit 缺 plugin/ 目录: ${PLUGIN_SRC_DIR}"
    return 1
  fi
  run mkdir -p "${PLUGIN_TARGET_DIR}"
  run cp "${PLUGIN_SRC_DIR}/index.ts" "${PLUGIN_TARGET_DIR}/index.ts"
  run cp "${PLUGIN_SRC_DIR}/openclaw.plugin.json" "${PLUGIN_TARGET_DIR}/openclaw.plugin.json"
  log_ok "plugin → ${PLUGIN_TARGET_DIR}"

  configure_plugin_via_openclaw
}

# ─────────────────────────────────────
# openclaw 集成(plugin 配置 / disable)
# ─────────────────────────────────────
locate_openclaw() {
  command -v openclaw 2>/dev/null && return 0
  [[ -x "${HOME}/.local/share/pnpm/openclaw" ]] && { echo "${HOME}/.local/share/pnpm/openclaw"; return 0; }
  return 1
}

configure_plugin_via_openclaw() {
  local bin; if ! bin="$(locate_openclaw)"; then
    log_skip "openclaw 未找到,跳过 plugin 默认配置写入"
    return 0
  fi
  if [[ "${DRY_RUN}" -eq 1 ]]; then
    printf '       (dry-run) %s config set plugins.entries.redskill.* (默认值)\n' "${bin}"
    return 0
  fi
  "${bin}" config set plugins.entries.redskill.enabled true
  "${bin}" config set plugins.entries.redskill.config.team 'rdc'
  "${bin}" config set plugins.entries.redskill.config.verbosity 'normal'
  log_ok "openclaw 配置已写入(team=rdc, verbosity=normal)"
}

disable_plugin_config() {
  local bin; if ! bin="$(locate_openclaw)"; then return 0; fi
  if [[ "${DRY_RUN}" -eq 1 ]]; then
    printf '       (dry-run) %s config unset plugins.entries.redskill\n' "${bin}"
    return 0
  fi
  "${bin}" config unset plugins.entries.redskill >/dev/null 2>&1 \
    && log_ok "已清理 openclaw plugin 配置项(避免与 skill 模式冲突)" \
    || log_skip "openclaw plugin 配置项不存在,无需清理"
}

# ─────────────────────────────────────
# 偏好持久化
# ─────────────────────────────────────
persist_skill_preference() {
  local enabled="$1"
  if ! command -v python3 >/dev/null 2>&1; then
    log_warn "python3 缺失,无法持久化 install_workspace_skills 偏好"
    return 0
  fi
  if [[ "${DRY_RUN}" -eq 1 ]]; then
    printf '       (dry-run) write install_workspace_skills=%s into %s\n' "${enabled}" "${CLI_CONFIG_TARGET}"
    return 0
  fi
  python3 - "${CLI_CONFIG_TARGET}" "${enabled}" <<'PY'
import json, sys
from pathlib import Path

p = Path(sys.argv[1]).expanduser()
on = sys.argv[2].strip().lower() == "true"

raw = {}
if p.exists():
    try:
        loaded = json.loads(p.read_text(encoding="utf-8"))
        if isinstance(loaded, dict):
            raw = loaded
    except Exception:
        raw = {}

raw["install_workspace_skills"] = on
p.parent.mkdir(parents=True, exist_ok=True)
p.write_text(json.dumps(raw, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
PY
  log_ok "偏好已写入: install_workspace_skills=${enabled} → ${CLI_CONFIG_TARGET}"
}

# ─────────────────────────────────────
# 可选:拉起 gateway
# ─────────────────────────────────────
maybe_restart_gateway() {
  [[ "${RESTART_GATEWAY}" -eq 1 ]] || return 0
  local bin; if ! bin="$(locate_openclaw)"; then
    log_warn "--restart-gateway 指定但找不到 openclaw,跳过"
    return 0
  fi
  if [[ "${DRY_RUN}" -eq 1 ]]; then
    printf '       (dry-run) %s gateway run --bind loopback --port 18789 --force\n' "${bin}"
    return 0
  fi
  nohup "${bin}" gateway run --bind loopback --port 18789 --force \
    >/tmp/openclaw-gateway.log 2>&1 &
  log_ok "openclaw gateway 已拉起(pid=$!,日志 /tmp/openclaw-gateway.log)"
}

# ─────────────────────────────────────
# 入口
# ─────────────────────────────────────
printf '== RedSkill kit installer ==\n'
printf '   components: %s%s\n' "${COMPONENTS}" "$([[ ${DRY_RUN} -eq 1 ]] && echo ' (dry-run)')"

want cli    && component_cli
want skill  && component_skill
want plugin && component_plugin

# skill 装了但 plugin 没装:显式清理同名 plugin 配置,避免 openclaw 报「插件被禁但 config 仍在」
if want skill && ! want plugin; then
  disable_plugin_config
fi

case "${SKILLS_PREF}" in
  on)  persist_skill_preference true  ;;
  off) persist_skill_preference false ;;
esac

maybe_restart_gateway

printf '\n'
log_done "完成。下面这条命令可以验:"
want cli    && printf '       redskill --version\n'
want skill  && printf '       ls %s %s\n' "${SKILL_FIND_TARGET}" "${SKILL_PREF_TARGET}"
want plugin && printf '       openclaw plugins list | grep redskill\n'
exit 0
