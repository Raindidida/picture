"""唯一感知后端 URL 的模块。

职责:
- URL 字段名常量 + TODO_FILL_ME 检查
- URL 模板 {slug} 替换 + URL encode
- HTTP 请求封装(超时、重试、流式上限、错误中文化)
- 统一返回对象 BundleResult / CliManifest

其它模块(installer / self_upgrade / redskill)只调本模块,
不接触 URL 字段名,不发原生 HTTP 请求。
"""
from __future__ import annotations

import json
import os
import random
import re
import socket
import time
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass
from typing import Optional
from urllib.parse import urlparse

import config


# ─────────────────────────────────────────
# URL 字段名 + TODO 占位
# ─────────────────────────────────────────
TODO_PLACEHOLDER = "TODO_FILL_ME"

URL_FIELD_GET_BUNDLE = "skills_primary_download_url_template"
URL_FIELD_SEARCH = "skills_search_url"
URL_FIELD_CLI_MANIFEST = "self_update_manifest_url"

_TODO_REF = {
    URL_FIELD_GET_BUNDLE: "T1",
    URL_FIELD_SEARCH: "T2",
    URL_FIELD_CLI_MANIFEST: "T3",
}


class UrlNotConfiguredError(Exception):
    def __init__(self, field: str):
        ref = _TODO_REF.get(field, "?")
        super().__init__(
            f"接口 {field} 尚未配置 (metadata.json 中为 {TODO_PLACEHOLDER})\n"
            f"       请联系小红书 RedSkill 后端负责人补全 URL,或参见 TODO.md {ref}。"
        )
        self.field = field


def _resolve_url(metadata: dict, field: str) -> str:
    url = (metadata.get(field) or "").strip()
    if not url or url == TODO_PLACEHOLDER:
        raise UrlNotConfiguredError(field)
    return url


def _build_bundle_url(template: str, identifier: str) -> str:
    """把 {slug} 替换为 URL-encoded identifier;无占位则附加为 query。"""
    encoded = urllib.parse.quote(identifier, safe="")
    if "{slug}" not in template:
        sep = "&" if "?" in template else "?"
        return f"{template}{sep}identifier={encoded}"
    return template.replace("{slug}", encoded)


# ─────────────────────────────────────────
# 大小上限
# ─────────────────────────────────────────
DOWNLOAD_MAX_BYTES = 100 * 1024 * 1024
JSON_MAX_BYTES = 5 * 1024 * 1024
_SHA256_RE = re.compile(r"^[0-9a-f]{64}$")


def _resolve_download_limit() -> int:
    raw = os.environ.get("REDSKILL_MAX_DOWNLOAD_MB", "").strip()
    if raw and raw.isdigit():
        return int(raw) * 1024 * 1024
    return DOWNLOAD_MAX_BYTES


def _validate_download_url(url: str, field: str) -> str:
    url = (url or "").strip()
    parsed = urlparse(url)
    if parsed.scheme not in ("http", "https") or not parsed.netloc:
        raise RuntimeError(f"{field} 下载地址非法,仅支持 http/https: {url!r}")
    return url


def _normalize_sha256(value: Optional[str], field: str, required: bool) -> Optional[str]:
    sha = (value or "").strip().lower()
    if not sha:
        if required:
            raise RuntimeError(
                f"{field} 缺少 sha256\n"
                f"       skill 包属于远程下发内容,生产环境必须提供 sha256。"
            )
        return None
    if not _SHA256_RE.match(sha):
        raise RuntimeError(f"{field} sha256 格式非法: {sha} (要求 64 位小写 hex)")
    return sha


# ─────────────────────────────────────────
# 网关信封拆封
# ─────────────────────────────────────────
def _unwrap_envelope(data, label: str):
    """小红书内部网关统一信封 {code, success, msg, data} 拆封。

    后端非信封返回时原样透传(向后兼容)。code != 0 / success=False 视为业务错。
    """
    if not isinstance(data, dict):
        return data
    if "data" in data and ("code" in data or "success" in data):
        code = data.get("code")
        success = data.get("success")
        if (code is not None and code != 0) or success is False:
            msg = (data.get("msg") or "").strip() or "未知后端错误"
            raise RuntimeError(f"{label} 后端返回失败: {msg} (code={code})")
        inner = data.get("data")
        if not isinstance(inner, dict):
            raise RuntimeError(f"{label} 信封 data 字段不是对象")
        return inner
    return data


# ─────────────────────────────────────────
# 统一返回对象
# ─────────────────────────────────────────
@dataclass
class BundleResult:
    identifier: str
    zip_bytes: Optional[bytes]
    zip_url: Optional[str]
    version: Optional[str]
    sha256: Optional[str]
    source: str = "redskill"
    name: Optional[str] = None


@dataclass
class CliManifest:
    version: str
    zip_url: str
    sha256: str
    release_notes: Optional[str] = None
    released_at: Optional[str] = None


# ─────────────────────────────────────────
# 通用 HTTP 客户端
# ─────────────────────────────────────────
DEFAULT_TIMEOUT = 30
MAX_RETRY = 2


def _build_headers(extra: dict = None) -> dict:
    headers = {
        "User-Agent": f"redskill-cli/{config.load_version()}",
        "Accept": "application/json, application/zip, */*",
    }
    # 二期在此处注入 SSO Cookie / X-User-Token
    if extra:
        headers.update(extra)
    return headers


def _format_http_error(e: urllib.error.HTTPError, url: str) -> RuntimeError:
    msg = ""
    try:
        body_bytes = e.read()
    except Exception:
        body_bytes = b""
    finally:
        try:
            e.close()
        except Exception:
            pass

    if body_bytes:
        try:
            body = json.loads(body_bytes.decode("utf-8"))
            if isinstance(body, dict):
                msg = str(body.get("message") or "").strip()
        except (json.JSONDecodeError, UnicodeDecodeError):
            pass

    if msg:
        return RuntimeError(f"{msg} (HTTP {e.code})")
    return RuntimeError(f"HTTP {e.code}: {e.reason} ({url})")


def _format_url_error(e: urllib.error.URLError, url: str, timeout: int) -> RuntimeError:
    reason = e.reason
    if isinstance(reason, socket.timeout) or "timed out" in str(reason).lower():
        return RuntimeError(f"请求超时 (>{timeout}s): {url}")
    if isinstance(reason, ConnectionRefusedError):
        return RuntimeError(f"网关拒绝连接 ({url}),可能服务未上线或域名错误")
    if isinstance(reason, socket.gaierror):
        return RuntimeError(f"DNS 解析失败 ({url}): {reason}")
    return RuntimeError(f"网络请求失败 ({url}): {reason}")


def _retry_sleep(attempt: int) -> None:
    base = 0.5 * (attempt + 1)
    time.sleep(base + random.random() * 0.5)


def _normalize_headers(headers) -> dict:
    return {str(k).lower(): v for k, v in headers.items()}


def _read_response_body(resp, max_bytes: int, headers: dict = None) -> bytes:
    resp_headers = headers if headers is not None else _normalize_headers(resp.headers)
    content_length = resp_headers.get("content-length")
    if content_length and content_length.isdigit() and int(content_length) > max_bytes:
        raise RuntimeError(
            f"响应体超过大小上限 ({int(content_length) / 1024 / 1024:.1f} MB "
            f"> {max_bytes / 1024 / 1024:.0f} MB)"
        )

    chunks = []
    total = 0
    while True:
        chunk = resp.read(64 * 1024)
        if not chunk:
            break
        total += len(chunk)
        if total > max_bytes:
            raise RuntimeError(
                f"响应体超过大小上限 ({total / 1024 / 1024:.1f} MB "
                f"> {max_bytes / 1024 / 1024:.0f} MB)"
            )
        chunks.append(chunk)
    return b"".join(chunks)


def _request(url: str, accept: str = None, timeout: int = DEFAULT_TIMEOUT,
             max_bytes: int = JSON_MAX_BYTES):
    """返回 (headers_dict, body_bytes)。

    重试策略:
    - 4xx:不重试,翻译错误抛出
    - 5xx / 超时 / 网络错误:重试 MAX_RETRY 次,退避 + jitter
    - 响应体按 max_bytes 流式读取,超限立即失败
    """
    headers = _build_headers({"Accept": accept} if accept else None)
    req = urllib.request.Request(url, headers=headers)

    last_err = None
    for attempt in range(MAX_RETRY + 1):
        try:
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                resp_headers = _normalize_headers(resp.headers)
                return resp_headers, _read_response_body(resp, max_bytes, resp_headers)
        except urllib.error.HTTPError as e:
            err = _format_http_error(e, url)
            if 400 <= e.code < 500:
                raise err
            last_err = err
        except urllib.error.URLError as e:
            last_err = _format_url_error(e, url, timeout)
        except TimeoutError:
            last_err = RuntimeError(f"请求超时 (>{timeout}s): {url}")
        except socket.timeout:
            last_err = RuntimeError(f"请求超时 (>{timeout}s): {url}")

        if attempt < MAX_RETRY:
            _retry_sleep(attempt)

    raise last_err if last_err else RuntimeError(f"未知请求错误: {url}")


# ─────────────────────────────────────────
# API-1 get_skill_bundle
# ─────────────────────────────────────────
def get_skill_bundle(identifier: str, metadata: dict) -> BundleResult:
    template = _resolve_url(metadata, URL_FIELD_GET_BUNDLE)
    url = _build_bundle_url(template, identifier)
    resp_headers, body = _request(
        url,
        accept="application/json, application/zip, */*",
        max_bytes=_resolve_download_limit(),
    )
    ctype = (resp_headers.get("content-type") or "").lower()
    allow_unsigned = os.environ.get("REDSKILL_ALLOW_UNSIGNED_BUNDLE") == "1"

    # 形态 A: zip 二进制
    if "application/zip" in ctype or body[:4] == b"PK\x03\x04":
        return BundleResult(
            identifier=identifier,
            zip_bytes=body,
            zip_url=None,
            version=resp_headers.get("x-skill-version") or None,
            sha256=_normalize_sha256(
                resp_headers.get("x-skill-sha256"),
                "get_skill_bundle 响应头 X-Skill-Sha256",
                required=not allow_unsigned,
            ),
        )

    # 形态 B: JSON manifest
    if "application/json" in ctype:
        try:
            data = json.loads(body.decode("utf-8"))
        except json.JSONDecodeError as e:
            raise RuntimeError(f"get_skill_bundle 返回非 JSON: {e}")
        if not isinstance(data, dict):
            raise RuntimeError("get_skill_bundle 返回顶层不是 JSON 对象")
        data = _unwrap_envelope(data, "get_skill_bundle")
        return BundleResult(
            identifier=identifier,
            zip_bytes=None,
            zip_url=_validate_download_url(data.get("zip_url"), "get_skill_bundle.zip_url"),
            version=data.get("version"),
            sha256=_normalize_sha256(
                data.get("sha256"),
                "get_skill_bundle.sha256",
                required=not allow_unsigned,
            ),
        )

    raise RuntimeError(f"未知响应类型: Content-Type={ctype}")


def download_bytes(url: str) -> bytes:
    """形态 B 的二次下载,供 installer 调用。"""
    url = _validate_download_url(url, "download_bytes.url")
    limit = _resolve_download_limit()
    _, body = _request(
        url,
        accept="application/octet-stream, application/zip, */*",
        timeout=60,
        max_bytes=limit,
    )
    return body


# ─────────────────────────────────────────
# API-2 search
# ─────────────────────────────────────────
def search(query: str, limit: int, metadata: dict) -> dict:
    q = (query or "").strip()
    if not q:
        raise ValueError("搜索关键词不能为空")
    if limit < 1 or limit > 100:
        raise ValueError("limit 超出范围: 1-100")

    base_url = _resolve_url(metadata, URL_FIELD_SEARCH)
    params = urllib.parse.urlencode({"q": q, "limit": limit, "page": 1})
    sep = "&" if "?" in base_url else "?"
    url = f"{base_url}{sep}{params}"
    _, body = _request(url, accept="application/json", max_bytes=JSON_MAX_BYTES)

    try:
        data = json.loads(body.decode("utf-8"))
    except json.JSONDecodeError as e:
        raise RuntimeError(f"search 接口返回非 JSON: {e}")
    if not isinstance(data, dict):
        raise RuntimeError("search 接口返回顶层不是 JSON 对象")
    data = _unwrap_envelope(data, "search")

    results = data.get("results")
    if not isinstance(results, list):
        raise RuntimeError("search 接口缺少 results 数组")
    return data


# ─────────────────────────────────────────
# API-3 cli manifest
# ─────────────────────────────────────────
def get_cli_manifest(metadata: dict) -> CliManifest:
    url = _resolve_url(metadata, URL_FIELD_CLI_MANIFEST)
    _, body = _request(url, accept="application/json")
    try:
        data = json.loads(body.decode("utf-8"))
    except json.JSONDecodeError as e:
        raise RuntimeError(f"cli_version 接口返回非 JSON: {e}")
    if not isinstance(data, dict):
        raise RuntimeError("cli_version 接口返回顶层不是 JSON 对象")
    data = _unwrap_envelope(data, "cli_version")

    version = (data.get("version") or "").strip()
    zip_url = _validate_download_url(data.get("zip_url"), "cli_version.zip_url")
    # CLI 自升级 sha256 默认强制必填(防 MITM 替换 CLI 代码)。
    # 仅本地联调可显式 REDSKILL_ALLOW_UNSIGNED_CLI=1 跳过。
    allow_unsigned_cli = os.environ.get("REDSKILL_ALLOW_UNSIGNED_CLI") == "1"
    sha256 = _normalize_sha256(
        data.get("sha256"), "cli_version.sha256", required=not allow_unsigned_cli
    ) or ""

    if not version:
        raise RuntimeError("cli_version 接口缺少必填字段: version")

    return CliManifest(
        version=version,
        zip_url=zip_url,
        sha256=sha256,
        release_notes=(data.get("release_notes") or None),
        released_at=(data.get("released_at") or None),
    )
