#!/usr/bin/env python3
"""Open Sophie Pallas from a desktop launcher, starting its local server once."""

import argparse
import os
import subprocess
import sys
import time
import urllib.error
import urllib.request
import webbrowser
from pathlib import Path


ROOT = Path(__file__).resolve().parent


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
    args = parser.parse_args()
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
