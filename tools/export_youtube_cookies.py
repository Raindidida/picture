import base64
import json
import os
import shutil
import sqlite3
import subprocess
import sys
import tempfile
from pathlib import Path

import win32crypt
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes


WINDOWS_EPOCH_OFFSET = 11644473600000000
CHROME_ROOT = Path(os.environ["LOCALAPPDATA"]) / "Google" / "Chrome" / "User Data"
DOMAINS = (
    "youtube.com",
    ".youtube.com",
    "google.com",
    ".google.com",
    "accounts.google.com",
)


def chrome_paths(profile: str) -> tuple[Path, Path]:
    return (
        CHROME_ROOT / "Local State",
        CHROME_ROOT / profile / "Network" / "Cookies",
    )


def get_aes_key(local_state_path: Path) -> bytes:
    state = json.loads(local_state_path.read_text(encoding="utf-8"))
    encrypted_key = base64.b64decode(state["os_crypt"]["encrypted_key"])[5:]
    return win32crypt.CryptUnprotectData(encrypted_key, None, None, None, 0)[1]


def copy_cookie_db(src: Path, dst: Path) -> None:
    try:
        shutil.copy2(src, dst)
        return
    except OSError:
        pass

    subprocess.run(
        ["esentutl", "/y", str(src), "/d", str(dst), "/o"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        check=False,
    )
    if dst.exists():
        return

    subprocess.run(
        [
            "robocopy",
            str(src.parent),
            str(dst.parent),
            src.name,
            "/R:0",
            "/W:0",
        ],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        check=False,
    )
    copied = dst.parent / src.name
    if copied.exists() and copied != dst:
        copied.replace(dst)

    if not dst.exists():
        raise RuntimeError("could not copy Chrome cookie database")


def decrypt_value(encrypted_value: bytes, aes_key: bytes) -> str:
    if not encrypted_value:
        return ""

    if encrypted_value.startswith((b"v10", b"v11", b"v20")):
        nonce = encrypted_value[3:15]
        ciphertext = encrypted_value[15:-16]
        tag = encrypted_value[-16:]
        cipher = Cipher(
            algorithms.AES(aes_key),
            modes.GCM(nonce, tag),
            backend=default_backend(),
        )
        decryptor = cipher.decryptor()
        return (decryptor.update(ciphertext) + decryptor.finalize()).decode(
            "utf-8", errors="replace"
        )

    return win32crypt.CryptUnprotectData(encrypted_value, None, None, None, 0)[
        1
    ].decode("utf-8", errors="replace")


def is_relevant_domain(host: str) -> bool:
    host = host.lower()
    return any(host == domain or host.endswith(domain) for domain in DOMAINS)


def to_unix_time(expires_utc: int) -> int:
    if not expires_utc:
        return 0
    return max(0, int((expires_utc - WINDOWS_EPOCH_OFFSET) / 1_000_000))


def export(profile: str, output: Path) -> int:
    local_state, cookies_db = chrome_paths(profile)
    if not local_state.exists() or not cookies_db.exists():
        raise FileNotFoundError(f"Chrome profile not found: {profile}")

    aes_key = get_aes_key(local_state)
    tmp_dir = Path(tempfile.mkdtemp(prefix="yt_cookies_"))
    tmp_db = tmp_dir / "Cookies"

    try:
        copy_cookie_db(cookies_db, tmp_db)
        conn = sqlite3.connect(f"file:{tmp_db}?mode=ro", uri=True)
        rows = conn.execute(
            """
            SELECT host_key, name, CAST(encrypted_value AS BLOB), path, expires_utc,
                   is_secure, is_httponly
            FROM cookies
            WHERE host_key LIKE '%youtube.com%'
               OR host_key LIKE '%google.com%'
            """
        ).fetchall()
        conn.close()

        lines = [
            "# Netscape HTTP Cookie File",
            "# Generated locally for yt-dlp; do not share.",
            "",
        ]
        written = 0
        for host, name, encrypted_value, path, expires_utc, secure, _httponly in rows:
            if not is_relevant_domain(host):
                continue
            try:
                value = decrypt_value(encrypted_value, aes_key)
            except Exception:
                continue
            if not value:
                continue
            include_subdomains = "TRUE" if host.startswith(".") else "FALSE"
            secure_text = "TRUE" if secure else "FALSE"
            expires = to_unix_time(expires_utc)
            lines.append(
                f"{host}\t{include_subdomains}\t{path}\t{secure_text}\t{expires}\t{name}\t{value}"
            )
            written += 1

        if written == 0:
            raise RuntimeError("no usable YouTube/Google cookies exported")

        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text("\n".join(lines) + "\n", encoding="utf-8")
        return written
    finally:
        shutil.rmtree(tmp_dir, ignore_errors=True)


if __name__ == "__main__":
    profile = sys.argv[1] if len(sys.argv) > 1 else "Default"
    output = Path(sys.argv[2]) if len(sys.argv) > 2 else Path("downloads/youtube_cookies.txt")
    count = export(profile, output)
    print(f"Exported cookie file: {output}")
