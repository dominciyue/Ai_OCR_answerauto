@echo off
chcp 65001 >nul
echo ==========================================
echo  创建完整发布包
echo ==========================================
echo.

cd /d "%~dp0"

if not exist "dist\AI_Answer_System.exe" (
    echo 错误：找不到 dist\AI_Answer_System.exe
    echo 请先运行打包命令！
    pause
    exit /b 1
)

echo 正在创建发布包...

REM 创建目录结构
mkdir "dist\AI_Answer_System_v1.0.1_Windows\config" 2>nul
mkdir "dist\AI_Answer_System_v1.0.1_Windows\docs" 2>nul

REM 复制主程序
copy "dist\AI_Answer_System.exe" "dist\AI_Answer_System_v1.0.1_Windows\" >nul

REM 复制配置文件
copy "config\config.example.yaml" "dist\AI_Answer_System_v1.0.1_Windows\config\" >nul

REM 复制文档
copy "README.md" "dist\AI_Answer_System_v1.0.1_Windows\" >nul
copy "LICENSE" "dist\AI_Answer_System_v1.0.1_Windows\" >nul
copy "CONFIG_GUIDE.md" "dist\AI_Answer_System_v1.0.1_Windows\" >nul

if exist "docs\QUICKSTART.md" copy "docs\QUICKSTART.md" "dist\AI_Answer_System_v1.0.1_Windows\docs\" >nul
if exist "docs\DeepSeek申请教程.md" copy "docs\DeepSeek申请教程.md" "dist\AI_Answer_System_v1.0.1_Windows\docs\" >nul

REM 创建使用说明
(
echo AI自动答题系统 v1.0.1
echo.
echo 快速开始：
echo 1. 双击运行 AI_Answer_System.exe
echo 2. 首次运行会弹出配置向导
echo 3. 选择AI提供商（推荐DeepSeek^)
echo 4. 输入API密钥
echo 5. 点击"保存并启动"
echo 6. 按F9开始截图答题
echo.
echo 推荐使用DeepSeek：
echo - 注册：https://platform.deepseek.com/
echo - 新用户送500万tokens
echo - 1000题≈¥1
echo.
echo 详细文档：
echo - README.md - 项目说明
echo - CONFIG_GUIDE.md - 配置指南
echo - docs\DeepSeek申请教程.md - API教程
echo.
echo GitHub: https://github.com/dominciyue/Ai_OCR_answerauto
echo.
echo 完全免费开源，MIT协议
) > "dist\AI_Answer_System_v1.0.1_Windows\使用说明.txt"

echo.
echo ✓ 发布包创建完成！
echo.
echo 位置：dist\AI_Answer_System_v1.0.1_Windows\
echo.
echo 包含文件：
echo   - AI_Answer_System.exe （主程序）
echo   - config\config.example.yaml （配置示例）
echo   - README.md （项目说明）
echo   - LICENSE （开源协议）
echo   - CONFIG_GUIDE.md （配置指南）
echo   - docs\ （文档目录）
echo   - 使用说明.txt
echo.
echo 接下来：
echo 1. 测试 AI_Answer_System.exe 是否正常
echo 2. 压缩整个文件夹为ZIP
echo 3. 上传到GitHub Release
echo.
pause
