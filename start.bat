@echo off
chcp 65001 >nul
echo ========================================
echo    AI自动答题系统 - 启动器
echo ========================================
echo.

REM 检查是否已配置
if not exist "config\config.yaml" (
    echo 检测到首次运行，启动配置向导...
    python config_wizard.py
) else (
    echo 启动主程序...
    python src/main.py
)

if errorlevel 1 (
    echo.
    echo 程序运行出错！
    pause
)
