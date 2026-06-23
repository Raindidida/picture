"""加载 version.json / metadata.json。

只加载 JSON 返回 dict / str,**不解释业务字段含义**。
URL 字段名和 TODO_FILL_ME 检查全部由 api.py 负责。
"""
from __future__ import annotations

import json
from pathlib import Path

REDSKILL_HOME = Path("~/.redskill").expanduser()


def load_metadata() -> dict:
    path = REDSKILL_HOME / "metadata.json"
    if not path.exists():
        raise RuntimeError(
            f"未找到 {path}\n"
            f"       请先运行 install.sh 完成初始化。"
        )
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        raise RuntimeError(
            f"metadata.json 格式损坏: {e}\n"
            f"       路径: {path}\n"
            f"       请重新运行 install.sh --reset-metadata 恢复默认。"
        )
    if not isinstance(data, dict):
        raise RuntimeError(f"metadata.json 顶层必须是 JSON 对象: {path}")
    return data


def load_version() -> str:
    path = REDSKILL_HOME / "version.json"
    if not path.exists():
        return "0.0.0"
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        if isinstance(data, dict):
            return data.get("version") or "0.0.0"
        return "0.0.0"
    except (json.JSONDecodeError, AttributeError):
        return "0.0.0"
