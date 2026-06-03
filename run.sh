#!/bin/bash

echo "========================================"
echo "   AI自动答题系统 - 启动程序"
echo "========================================"
echo

# 检查配置文件
if [ ! -f "config/config.yaml" ]; then
    echo "❌ 配置文件不存在！"
    echo
    echo "请先执行以下操作："
    echo "1. 复制 config/config.example.yaml 为 config/config.yaml"
    echo "2. 编辑 config/config.yaml 填入你的API密钥"
    echo
    exit 1
fi

# 启动程序
python3 src/main.py

if [ $? -ne 0 ]; then
    echo
    echo "❌ 程序运行出错"
    echo "请查看上方错误信息"
    echo
fi
