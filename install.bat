@echo off
chcp 65001 >nul
echo ========================================
echo    AI自动答题系统 - 依赖安装脚本
echo ========================================
echo.

echo [1/3] 检查Python环境...
python --version
if errorlevel 1 (
    echo ❌ Python未安装或未添加到PATH
    echo 请先安装Python 3.8+
    pause
    exit /b 1
)
echo.

echo [2/3] 升级pip...
python -m pip install --upgrade pip
echo.

echo [3/3] 安装依赖包...
echo 这可能需要几分钟，请耐心等待...
echo.

pip install -r requirements.txt

if errorlevel 1 (
    echo.
    echo ❌ 依赖安装失败
    echo.
    echo 常见问题解决：
    echo 1. PaddlePaddle安装失败：访问 https://www.paddlepaddle.org.cn/ 选择合适版本
    echo 2. 缺少编译工具：需要安装 Microsoft Visual C++ 14.0+
    echo 3. 网络问题：可以使用国内镜像源
    echo    pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
    echo.
    pause
    exit /b 1
)

echo.
echo ========================================
echo ✅ 安装完成！
echo ========================================
echo.
echo 下一步：
echo 1. 编辑 config/config.yaml 填入你的API密钥
echo 2. 运行 python src/main.py 启动程序
echo.
pause
