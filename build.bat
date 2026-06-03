@echo off
chcp 65001 >nul
echo ========================================
echo    打包AI自动答题系统为EXE
echo ========================================
echo.

echo [1/3] 检查PyInstaller...
pip show pyinstaller >nul 2>&1
if errorlevel 1 (
    echo PyInstaller未安装，正在安装...
    pip install pyinstaller
)
echo.

echo [2/3] 清理旧的构建文件...
if exist "dist" rmdir /s /q dist
if exist "build" rmdir /s /q build
if exist "*.spec" del /q *.spec
echo.

echo [3/3] 开始打包...
echo 这可能需要几分钟，请耐心等待...
echo.

pyinstaller --onefile ^
    --windowed ^
    --name "AI答题系统" ^
    --icon=icon.ico ^
    --add-data "config;config" ^
    src/main.py

if errorlevel 1 (
    echo.
    echo ❌ 打包失败
    pause
    exit /b 1
)

echo.
echo ========================================
echo ✅ 打包完成！
echo ========================================
echo.
echo 生成的EXE文件位于: dist\AI答题系统.exe
echo.
echo 使用说明：
echo 1. 复制 config/config.yaml 到与EXE同目录的 config 文件夹
echo 2. 编辑配置文件填入你的API密钥
echo 3. 双击运行 AI答题系统.exe
echo.
pause
