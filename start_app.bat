@echo off
chcp 65001 > nul
title E-məktəb - Respublika Portalı

echo ========================================================
echo   E-MƏKTƏB (RESPUBLİKA ELEKTRON MƏKTƏB SİSTEMİ)
echo ========================================================
echo.
echo Server və Onlayn Tunel başladılır...
echo.

cd /d "%~dp0"

start /b python server.py
timeout /t 2 > nul

if exist cloudflared.exe (
    start "E-məktəb Online Tunnel" cloudflared.exe tunnel --url http://127.0.0.1:8000
)

:: Open in App Mode (Dedicated clean window)
start msedge --app=http://localhost:8000 2>nul || start chrome --app=http://localhost:8000 2>nul || start http://localhost:8000

echo.
echo Sistem aktivdir!
echo Proqramı dayandırmaq üçün bu pəncərəni bağlaya bilərsiniz.
echo ========================================================
pause
