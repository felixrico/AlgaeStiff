@echo off
REM Wrapper to run the PowerShell build script
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0build_windows.ps1" %*
