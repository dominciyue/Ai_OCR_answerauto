# AI Answer System - Create Release Package
# PowerShell Script

Write-Host "==========================================" -ForegroundColor Green
Write-Host " Creating Release Package" -ForegroundColor Green
Write-Host "==========================================" -ForegroundColor Green
Write-Host ""

# Check if EXE exists
if (-not (Test-Path "dist\AI_Answer_System.exe")) {
    Write-Host "ERROR: dist\AI_Answer_System.exe not found!" -ForegroundColor Red
    Write-Host "Please run the build command first!" -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host "Creating release package..." -ForegroundColor Cyan

# Create directory structure
$releaseDir = "dist\AI_Answer_System_v1.0.1_Windows"
New-Item -ItemType Directory -Force -Path "$releaseDir\config" | Out-Null
New-Item -ItemType Directory -Force -Path "$releaseDir\docs" | Out-Null

# Copy main program
Copy-Item "dist\AI_Answer_System.exe" "$releaseDir\" -Force

# Copy config
Copy-Item "config\config.example.yaml" "$releaseDir\config\" -Force

# Copy documentation
Copy-Item "README.md" "$releaseDir\" -Force -ErrorAction SilentlyContinue
Copy-Item "LICENSE" "$releaseDir\" -Force -ErrorAction SilentlyContinue
Copy-Item "CONFIG_GUIDE.md" "$releaseDir\" -Force -ErrorAction SilentlyContinue

if (Test-Path "docs\QUICKSTART.md") {
    Copy-Item "docs\QUICKSTART.md" "$releaseDir\docs\" -Force
}
if (Test-Path "docs\DeepSeek申请教程.md") {
    Copy-Item "docs\DeepSeek申请教程.md" "$releaseDir\docs\" -Force
}

# Create usage instructions
$usageText = @"
AI自动答题系统 v1.0.1

快速开始：
1. 双击运行 AI_Answer_System.exe
2. 首次运行会弹出配置向导
3. 选择AI提供商（推荐DeepSeek）
4. 输入API密钥
5. 点击"保存并启动"
6. 按F9开始截图答题

推荐使用DeepSeek：
- 注册：https://platform.deepseek.com/
- 新用户送500万tokens
- 1000题≈¥1

详细文档：
- README.md - 项目说明
- CONFIG_GUIDE.md - 配置指南
- docs\DeepSeek申请教程.md - API教程

GitHub: https://github.com/dominciyue/Ai_OCR_answerauto

完全免费开源，MIT协议
"@

$usageText | Out-File -FilePath "$releaseDir\使用说明.txt" -Encoding UTF8

Write-Host ""
Write-Host "✓ Release package created successfully!" -ForegroundColor Green
Write-Host ""
Write-Host "Location: $releaseDir" -ForegroundColor Cyan
Write-Host ""
Write-Host "Package contents:" -ForegroundColor Yellow
Write-Host "  - AI_Answer_System.exe (Main program)"
Write-Host "  - config\config.example.yaml (Config template)"
Write-Host "  - README.md (Documentation)"
Write-Host "  - LICENSE (MIT License)"
Write-Host "  - CONFIG_GUIDE.md (Config guide)"
Write-Host "  - docs\ (Documentation folder)"
Write-Host "  - 使用说明.txt (Quick start)"
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host "1. Test: cd $releaseDir; .\AI_Answer_System.exe"
Write-Host "2. Compress: Compress-Archive -Path '$releaseDir' -DestinationPath '$releaseDir.zip'"
Write-Host "3. Upload to GitHub Release"
Write-Host ""
Read-Host "Press Enter to exit"
