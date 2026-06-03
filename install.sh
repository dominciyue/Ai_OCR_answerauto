#!/bin/bash

echo "========================================"
echo "   AI自动答题系统 - 依赖安装脚本"
echo "========================================"
echo

echo "[1/3] 检查Python环境..."
python3 --version
if [ $? -ne 0 ]; then
    echo "❌ Python未安装"
    echo "请先安装Python 3.8+"
    exit 1
fi
echo

echo "[2/3] 升级pip..."
python3 -m pip install --upgrade pip
echo

echo "[3/3] 安装依赖包..."
echo "这可能需要几分钟，请耐心等待..."
echo

pip3 install -r requirements.txt

if [ $? -ne 0 ]; then
    echo
    echo "❌ 依赖安装失败"
    echo
    echo "常见问题解决："
    echo "1. PaddlePaddle安装失败：访问 https://www.paddlepaddle.org.cn/ 选择合适版本"
    echo "2. 网络问题：可以使用国内镜像源"
    echo "   pip3 install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple"
    echo
    exit 1
fi

echo
echo "========================================"
echo "✅ 安装完成！"
echo "========================================"
echo
echo "下一步："
echo "1. 编辑 config/config.yaml 填入你的API密钥"
echo "2. 运行 python3 src/main.py 启动程序"
echo
