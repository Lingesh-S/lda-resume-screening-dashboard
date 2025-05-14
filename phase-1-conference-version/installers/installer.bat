@echo off
setlocal
echo "Downloading python"
REM Download Python installer
curl -LO https://www.python.org/ftp/python/3.10.10/python-3.10.10-amd64.exe

echo "python installation done"

REM Install Python silently
start /wait python-3.10.10-amd64.exe /quiet InstallAllUsers=1 PrependPath=1

REM Add Python to the system's PATH environment variable
setx PATH "%PATH%;C:\Python310;C:\Python310\Scripts"
del  python-3.10.10-amd64.exe

endlocal