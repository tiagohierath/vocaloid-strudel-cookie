@echo off
setlocal
cd /d "%~dp0"

rem Use an existing Python install when available.
where py >nul 2>nul
if not errorlevel 1 goto system_py
where python >nul 2>nul
if not errorlevel 1 goto system_python

rem Otherwise download a private, no-admin Python runtime for this app.
set "RUNTIME_ROOT=%LOCALAPPDATA%\Sophie Pallas\runtime"
set "RUNTIME_ZIP=%TEMP%\sophie-pallas-python.zip"
if exist "%RUNTIME_ROOT%\python.exe" goto embedded_python
echo Downloading the small private Python runtime...
powershell -NoProfile -ExecutionPolicy Bypass -Command "$ProgressPreference='SilentlyContinue'; New-Item -ItemType Directory -Force -Path '%RUNTIME_ROOT%' | Out-Null; Invoke-WebRequest -UseBasicParsing -Uri 'https://www.python.org/ftp/python/3.12.8/python-3.12.8-embed-amd64.zip' -OutFile '%RUNTIME_ZIP%'; Expand-Archive -Force -Path '%RUNTIME_ZIP%' -DestinationPath '%RUNTIME_ROOT%'; Remove-Item -Force '%RUNTIME_ZIP%'"
if errorlevel 1 (
  echo Could not download Python. Check your internet connection and try again.
  pause
  exit /b 1
)

:embedded_python
set "SOPHIE_RUNTIME=%RUNTIME_ROOT%"
"%RUNTIME_ROOT%\python.exe" "%~dp0install.py"
goto finished

:system_py
py -3 "%~dp0install.py"
goto finished

:system_python
python "%~dp0install.py"

:finished
if errorlevel 1 pause
endlocal
