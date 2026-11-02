#!/usr/bin/env python3
"""Install Sophie Pallas for the current user and open it."""

import os
import shutil
import subprocess
import sys
from pathlib import Path


APP_NAME = "Sophie Pallas"
SOURCE = Path(__file__).resolve().parent
FILES = (
    "index.html",
    "dials.js",
    "girl-reference.png",
    "serve.py",
    "launch.py",
    "run.sh",
    "run.bat",
    "VERSION",
    "README.md",
    "docs/RUNNING.md",
)


def install_root() -> Path:
    if os.name == "nt":
        return Path(os.environ.get("LOCALAPPDATA", Path.home() / "AppData/Local")) / APP_NAME
    return Path(os.environ.get("XDG_DATA_HOME", Path.home() / ".local/share")) / "sophie-pallas"


def app_root() -> Path:
    return install_root() / "app"


def copy_app() -> Path:
    target = app_root()
    target.mkdir(parents=True, exist_ok=True)
    for relative in FILES:
        source = SOURCE / relative
        destination = target / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, destination)
    if os.name != "nt":
        (target / "run.sh").chmod(0o755)
    return target


def python_executable(target: Path) -> Path:
    bundled = os.environ.get("SOPHIE_RUNTIME")
    if bundled:
        candidate = Path(bundled) / ("pythonw.exe" if os.name == "nt" else "python3")
        if candidate.exists():
            return candidate
    return Path(sys.executable)


def create_windows_shortcuts(target: Path, executable: Path) -> None:
    if os.name != "nt":
        return
    start_menu = Path(os.environ.get("APPDATA", Path.home())) / "Microsoft/Windows/Start Menu/Programs"
    desktop = Path(os.environ.get("USERPROFILE", Path.home())) / "Desktop"
    start_menu.mkdir(parents=True, exist_ok=True)
    desktop.mkdir(parents=True, exist_ok=True)
    script = """
$shell = New-Object -ComObject WScript.Shell
foreach ($path in @($env:SOPHIE_DESKTOP, $env:SOPHIE_START)) {
  $shortcut = $shell.CreateShortcut($path)
  $shortcut.TargetPath = $env:SOPHIE_PYTHON
  $shortcut.Arguments = ('"' + $env:SOPHIE_LAUNCH + '"')
  $shortcut.WorkingDirectory = $env:SOPHIE_APP
  $shortcut.IconLocation = ($env:SOPHIE_APP + '\\girl-reference.png')
  $shortcut.Save()
}
"""
    environment = os.environ.copy()
    environment.update(
        {
            "SOPHIE_DESKTOP": str(desktop / f"{APP_NAME}.lnk"),
            "SOPHIE_START": str(start_menu / f"{APP_NAME}.lnk"),
            "SOPHIE_PYTHON": str(executable),
            "SOPHIE_LAUNCH": str(target / "launch.py"),
            "SOPHIE_APP": str(target),
        }
    )
    subprocess.run(
        ["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-Command", script],
        env=environment,
        check=True,
        creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0),
    )


def create_linux_desktop_file(target: Path, executable: Path) -> None:
    if os.name == "nt":
        return
    data_home = Path(os.environ.get("XDG_DATA_HOME", Path.home() / ".local/share"))
    applications = data_home / "applications"
    applications.mkdir(parents=True, exist_ok=True)
    desktop = applications / "sophie-pallas.desktop"
    launch = target / "launch.py"
    desktop.write_text(
        "\n".join(
            [
                "[Desktop Entry]",
                "Type=Application",
                f"Name={APP_NAME}",
                "Comment=Make a loop with Mimi and a tiny synth rack",
                f'Exec="{executable}" "{launch}"',
                f"Icon={target / 'girl-reference.png'}",
                "Terminal=false",
                "Categories=AudioVideo;Audio;Game;",
                "Keywords=music;synth;loop;Mimi;Sophie;",
                "",
            ]
        ),
        encoding="utf-8",
    )
    update_database = shutil.which("update-desktop-database")
    if update_database:
        subprocess.run([update_database, str(applications)], check=False)


def uninstall() -> None:
    shutil.rmtree(install_root(), ignore_errors=True)
    if os.name != "nt":
        desktop = Path(os.environ.get("XDG_DATA_HOME", Path.home() / ".local/share")) / "applications/sophie-pallas.desktop"
        desktop.unlink(missing_ok=True)


def main() -> int:
    if "--uninstall" in sys.argv:
        uninstall()
        return 0
    target = copy_app()
    executable = python_executable(target)
    create_windows_shortcuts(target, executable)
    create_linux_desktop_file(target, executable)
    launch = target / "launch.py"
    if os.name == "nt":
        subprocess.Popen([str(executable), str(launch)], cwd=target)
    else:
        subprocess.Popen([str(executable), str(launch)], cwd=target, start_new_session=True)
    print(f"Installed {APP_NAME} to {target}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
