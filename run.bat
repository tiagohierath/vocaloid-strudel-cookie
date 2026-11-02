@echo off
setlocal
cd /d "%~dp0"

where py >nul 2>nul
if not errorlevel 1 goto launch_py
where python >nul 2>nul
if not errorlevel 1 goto launch_python

echo Sophie Pallas needs Python 3.
echo Install it from https://www.python.org/downloads/windows/
pause
exit /b 1

:launch_py
py -3 serve.py %*
goto done

:launch_python
python serve.py %*

:done

endlocal
