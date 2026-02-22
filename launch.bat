@echo off
cd /d D:\SENDS

:: node_modules 없으면 설치
if not exist "node_modules" (
    echo 패키지 설치 중...
    npm install
)

:: 서버 새 창으로 실행
start "건설안전기술사 서버" cmd /k "cd /d D:\SENDS && node server.js"

:: 브라우저 열기 (서버 기동 대기)
timeout /t 2 /nobreak > nul
start http://localhost:3840/
