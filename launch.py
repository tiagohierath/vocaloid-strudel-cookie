#!/usr/bin/env python3
"""Start Sophie Pallas and quietly install GitHub releases when available."""

import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
import time
import urllib.error
import urllib.request
import webbrowser
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parent
REPOSITORY = "tiagohierath/vocaloid-strudel-cookie"
RELEASES_API = f"https://api.github.com/repos/{REPOSITORY}/releases/latest"
UPDATE_INTERVAL = 6 * 60 * 60
MAX_UPDATE_SIZE = 50 * 1024 * 1024
UPDATE_FILES = (
    "index.html",
    "dials.js",
    "girl-reference.png",
    "serve.py",
    "launch.py",
    "run.sh",
    "run.bat",
    "VERSION",
)


def version_tuple(value: str):
    value = value.strip().lstrip("v")
    parts = value.split(".")
    if len(parts) != 3 or not all(part.isdigit() for part in parts):
        return (0, 0, 0)
    return tuple(int(part) for part in parts)


def read_version() -> str:
    try:
        return (ROOT / "VERSION").read_text(encoding="utf-8").strip()
    except OSError:
        return "0.0.0"


def state_file() -> Path:
    if os.name == "nt":
        base = Path(os.environ.get("LOCALAPPDATA", Path.home() / "AppData/Local"))
    else:
        base = Path(os.environ.get("XDG_STATE_HOME", Path.home() / ".local/state"))
    return base / "sophie-pallas" / "update.json"


def load_state() -> dict:
    try:
        return json.loads(state_file().read_text(encoding="utf-8"))
    except (OSError, ValueError, TypeError):
        return {}


def save_state(**updates) -> None:
    path = state_file()
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        state = load_state()
        state.update(updates)
        path.write_text(json.dumps(state, indent=2), encoding="utf-8")
    except OSError:
        pass


def should_check(force: bool) -> bool:
    if force:
        return True
    try:
        return time.time() - float(load_state().get("checked_at", 0)) >= UPDATE_INTERVAL
    except (TypeError, ValueError):
        return True


def request_json(url: str) -> dict:
    request = urllib.request.Request(
        url,
        headers={"Accept": "application/vnd.github+json", "User-Agent": "Sophie-Pallas-Updater"},
    )
    with urllib.request.urlopen(request, timeout=8) as response:
        return json.loads(response.read())


def download(url: str, destination: Path) -> None:
    request = urllib.request.Request(url, headers={"User-Agent": "Sophie-Pallas-Updater"})
    with urllib.request.urlopen(request, timeout=30) as response, destination.open("wb") as output:
        total = 0
        while True:
            chunk = response.read(1024 * 256)
            if not chunk:
                break
            total += len(chunk)
            if total > MAX_UPDATE_SIZE:
                raise RuntimeError("update package is too large")
            output.write(chunk)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for chunk in iter(lambda: source.read(1024 * 256), b""):
            digest.update(chunk)
    return digest.hexdigest()


def expected_digest(asset: dict, assets_by_name: dict) -> str | None:
    digest = asset.get("digest") or ""
    if digest.startswith("sha256:"):
        return digest.split(":", 1)[1].strip().lower()
    sidecar = assets_by_name.get(f"{asset.get('name')}.sha256")
    if sidecar:
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / "checksum.txt"
            download(sidecar["browser_download_url"], path)
            text = path.read_text(encoding="utf-8").strip().split()
            if text:
                return text[0].lower()
    return None


def install_release(archive: Path) -> None:
    with tempfile.TemporaryDirectory() as temporary:
        extract_root = Path(temporary).resolve()
        with zipfile.ZipFile(archive) as package:
            for member in package.infolist():
                target = (extract_root / member.filename).resolve()
                if not str(target).startswith(str(extract_root) + os.sep):
                    raise RuntimeError("invalid update archive")
            package.extractall(extract_root)

        candidates = {path.name: path for path in extract_root.rglob("*") if path.is_file()}
        missing = [name for name in UPDATE_FILES if name not in candidates]
        if missing:
            raise RuntimeError(f"update is missing: {', '.join(missing)}")

        for name in UPDATE_FILES:
            source = candidates[name]
            destination = ROOT / name
            destination.parent.mkdir(parents=True, exist_ok=True)
            temporary_destination = destination.with_name(f".{destination.name}.update")
            shutil.copy2(source, temporary_destination)
            os.replace(temporary_destination, destination)


def maybe_update(force: bool = False) -> str:
    # A source checkout belongs to the developer. Only managed installs self-update.
    if (ROOT / ".git").exists() or not should_check(force):
        return ""
    current = read_version()
    try:
        release = request_json(RELEASES_API)
        tag = str(release.get("tag_name", ""))
        save_state(checked_at=time.time(), latest=tag)
        if version_tuple(tag) <= version_tuple(current):
            return ""
        assets = {asset.get("name"): asset for asset in release.get("assets", [])}
        asset = assets.get(f"sophie-pallas-{tag}.zip")
        if not asset:
            return ""
        with tempfile.TemporaryDirectory() as temporary:
            archive = Path(temporary) / asset["name"]
            download(asset["browser_download_url"], archive)
            expected = expected_digest(asset, assets)
            if expected and sha256(archive) != expected:
                raise RuntimeError("update checksum does not match")
            install_release(archive)
            save_state(installed=tag)
        return tag
    except (OSError, RuntimeError, ValueError, KeyError, TypeError, urllib.error.URLError, zipfile.BadZipFile):
        save_state(checked_at=time.time(), error="update failed")
        return ""


def sophie_is_running(url: str) -> bool:
    try:
        with urllib.request.urlopen(url, timeout=0.35) as response:
            return response.status == 200 and b"Sophie Pallas" in response.read(8192)
    except (OSError, urllib.error.URLError):
        return False


def start_server(port: int) -> None:
    command = [sys.executable, str(ROOT / "serve.py"), "--port", str(port)]
    options = {
        "cwd": ROOT,
        "stdin": subprocess.DEVNULL,
        "stdout": subprocess.DEVNULL,
        "stderr": subprocess.DEVNULL,
    }
    if os.name == "nt":
        options["creationflags"] = subprocess.CREATE_NEW_PROCESS_GROUP | subprocess.DETACHED_PROCESS
    else:
        options["start_new_session"] = True
    subprocess.Popen(command, **options)


def main() -> int:
    parser = argparse.ArgumentParser(description="Open Sophie Pallas")
    parser.add_argument("--port", type=int, default=5175)
    parser.add_argument("--check-updates", action="store_true")
    args = parser.parse_args()
    maybe_update(args.check_updates)
    url = f"http://127.0.0.1:{args.port}/"

    if not sophie_is_running(url):
        start_server(args.port)
        for _ in range(30):
            if sophie_is_running(url):
                break
            time.sleep(0.1)

    webbrowser.open_new_tab(url)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
