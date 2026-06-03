"""
简化版测试 - 手动输入题目文本测试DeepSeek
"""
import sys
import yaml
from pathlib import Path
import io

# 设置UTF-8编码输出
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# 添加项目根目录到路径
ROOT_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT_DIR))

from src.ai_client import AIClient

def load_config():
    """加载配置文件"""
    config_path = Path("config/config.yaml")
    with open(config_path, 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f)
    return config

def main():
    print("=" * 60)
    print("AI自动答题系统 - 简化测试版")
    print("=" * 60)

    # 加载配置
    config = load_config()
    print(f"\n配置信息:")
    print(f"  AI提供商: {config['ai']['provider']}")
    print(f"  模型: {config['ai']['model']}")
    print(f"  API密钥: {config['ai']['api_key'][:20]}...")

    # 初始化AI客户端
    print("\n正在初始化AI客户端...")
    ai_client = AIClient(config)
    print("AI客户端初始化成功！\n")

    print("=" * 60)
    print("请输入题目内容（输入'exit'退出）:")
    print("=" * 60)

    while True:
        print("\n题目:")
        question = input()

        if question.lower() == 'exit':
            print("\n再见！")
            break

        if not question.strip():
            print("题目不能为空，请重新输入")
            continue

        print("\n正在请求AI回答...")
        print("-" * 60)

        try:
            answer = ai_client.answer_question(question)
            if answer:
                print("\nAI回答:")
                print("=" * 60)
                print(answer)
                print("=" * 60)
            else:
                print("\n❌ AI回答失败")
        except Exception as e:
            print(f"\n❌ 错误: {e}")

if __name__ == "__main__":
    main()
