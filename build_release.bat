@echo off
chcp 65001 >nul
echo ========================================
echo    AI自动答题系统 - 完整打包脚本
echo ========================================
echo.

REM 1. 检查环境
echo [1/5] 检查环境...
python --version
if errorlevel 1 (
    echo ❌ Python未安装
    pause
    exit /b 1
)

pip show pyinstaller >nul 2>&1
if errorlevel 1 (
    echo PyInstaller未安装，正在安装...
    pip install pyinstaller
)
echo.

REM 2. 清理旧文件
echo [2/5] 清理旧文件...
if exist "dist" rmdir /s /q dist
if exist "build" rmdir /s /q build
if exist "*.spec" del /q *.spec
echo.

REM 3. 打包主程序
echo [3/5] 打包主程序...
echo 这可能需要5-10分钟，请耐心等待...
echo.

pyinstaller --noconfirm ^
    --onefile ^
    --windowed ^
    --name "AI答题系统" ^
    --add-data "config/config.example.yaml;config" ^
    --hidden-import "rapidocr_onnxruntime" ^
    --hidden-import "PIL" ^
    --hidden-import "mss" ^
    --hidden-import "keyboard" ^
    --collect-data "rapidocr_onnxruntime" ^
    src/main.py

if errorlevel 1 (
    echo.
    echo ❌ 打包失败
    pause
    exit /b 1
)
echo.

REM 4. 创建发布包
echo [4/5] 创建发布包...
mkdir "dist\AI答题系统_v1.0.0_Windows" 2>nul
mkdir "dist\AI答题系统_v1.0.0_Windows\config" 2>nul
mkdir "dist\AI答题系统_v1.0.0_Windows\docs" 2>nul

copy "dist\AI答题系统.exe" "dist\AI答题系统_v1.0.0_Windows\" >nul
copy "config\config.example.yaml" "dist\AI答题系统_v1.0.0_Windows\config\" >nul
copy "README.md" "dist\AI答题系统_v1.0.0_Windows\" >nul
copy "LICENSE" "dist\AI答题系统_v1.0.0_Windows\" >nul
copy "docs\QUICKSTART.md" "dist\AI答题系统_v1.0.0_Windows\docs\" >nul
copy "docs\DeepSeek申请教程.md" "dist\AI答题系统_v1.0.0_Windows\docs\" >nul

REM 创建启动说明
echo AI自动答题系统 > "dist\AI答题系统_v1.0.0_Windows\使用说明.txt"
echo. >> "dist\AI答题系统_v1.0.0_Windows\使用说明.txt"
echo 首次使用： >> "dist\AI答题系统_v1.0.0_Windows\使用说明.txt"
echo 1. 双击运行 AI答题系统.exe >> "dist\AI答题系统_v1.0.0_Windows\使用说明.txt"
echo 2. 首次启动会弹出配置向导 >> "dist\AI答题系统_v1.0.0_Windows\使用说明.txt"
echo 3. 选择 DeepSeek 并填入API Key >> "dist\AI答题系统_v1.0.0_Windows\使用说明.txt"
echo 4. 保存配置并启动 >> "dist\AI答题系统_v1.0.0_Windows\使用说明.txt"
echo 5. 按 F9 开始使用 >> "dist\AI答题系统_v1.0.0_Windows\使用说明.txt"
echo. >> "dist\AI答题系统_v1.0.0_Windows\使用说明.txt"
echo 详细文档：README.md >> "dist\AI答题系统_v1.0.0_Windows\使用说明.txt"
echo DeepSeek申请：docs\DeepSeek申请教程.md >> "dist\AI答题系统_v1.0.0_Windows\使用说明.txt"
echo. >> "dist\AI答题系统_v1.0.0_Windows\使用说明.txt"
echo 项目地址：https://github.com/dominciyue/Ai_OCR_answerauto >> "dist\AI答题系统_v1.0.0_Windows\使用说明.txt"

echo.

REM 5. 压缩打包
echo [5/5] 压缩打包...
if exist "C:\Program Files\7-Zip\7z.exe" (
    "C:\Program Files\7-Zip\7z.exe" a -tzip "dist\AI答题系统_v1.0.0_Windows.zip" "dist\AI答题系统_v1.0.0_Windows\*"
    echo ✅ 已创建压缩包
) else (
    echo ⚠️  未找到7-Zip，请手动压缩 dist\AI答题系统_v1.0.0_Windows 文件夹
)

echo.
echo ========================================
echo ✅ 打包完成！
echo ========================================
echo.
echo 发布文件位于：
echo - dist\AI答题系统_v1.0.0_Windows\
echo - dist\AI答题系统_v1.0.0_Windows.zip （如果安装了7-Zip）
echo.
echo 文件大小约：30-50MB
echo.
echo 测试清单：
echo [ ] 双击运行EXE
echo [ ] 测试配置向导
echo [ ] 测试截图功能（F9）
echo [ ] 测试OCR识别
echo [ ] 测试AI回答
echo [ ] 测试历史记录
echo [ ] 测试快捷键设置
echo.
echo 发布到GitHub：
echo 1. 访问 https://github.com/dominciyue/Ai_OCR_answerauto/releases
echo 2. 点击 "Create a new release"
echo 3. Tag: v1.0.0
echo 4. Title: AI自动答题系统 v1.0.0
echo 5. 上传 AI答题系统_v1.0.0_Windows.zip
echo 6. 复制 RELEASE_v1.0.0.md 的内容作为说明
echo.
pause
