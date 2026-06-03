@echo off
chcp 65001 >nul
echo ========================================
echo    AI自动答题系统 - 启动程序
echo ========================================
echo.

REM 检查配置文件
if not exist "config\config.yaml" (
    echo ❌ 配置文件不存在！
    echo.
    echo 请先执行以下操作：
    echo 1. 复制 config\config.example.yaml 为 config\config.yaml
    echo 2. 编辑 config\config.yaml 填入你的API密钥
    echo.
    pause
    exit /b 1
)

REM 启动程序
python src\main.py

if errorlevel 1 (
    echo.
    echo ❌ 程序运行出错
    echo 请查看上方错误信息
    echo.
    pause
)
