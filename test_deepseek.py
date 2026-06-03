"""
测试DeepSeek API连接
"""
import sys
import yaml
from pathlib import Path

# 设置UTF-8编码
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# 尝试导入openai
try:
    from openai import OpenAI
    print("✅ openai库已安装")
except ImportError:
    print("❌ openai库未安装，正在尝试安装...")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "openai"])
    from openai import OpenAI
    print("✅ openai库安装完成")

# 加载配置
config_path = Path("config/config.yaml")
with open(config_path, 'r', encoding='utf-8') as f:
    config = yaml.safe_load(f)

api_key = config['ai']['api_key']
model = config['ai']['model']
base_url = config['ai']['base_url']

print("\n" + "="*50)
print("配置信息:")
print(f"   API Key: {api_key[:20]}...")
print(f"   Model: {model}")
print(f"   Base URL: {base_url}")
print("="*50 + "\n")

# 初始化客户端
print("正在连接DeepSeek API...")
client = OpenAI(
    api_key=api_key,
    base_url=base_url,
    timeout=30
)

# 测试简单问题
test_question = """
以下哪项是Python的特点？
A. 静态类型
B. 动态类型
C. 编译型语言
D. 不支持面向对象
"""

print(f"测试问题:\n{test_question}")
print("\n正在请求AI回答...\n")

try:
    response = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "system",
                "content": "你是一个专业、准确的答题助手。"
            },
            {
                "role": "user",
                "content": f"请回答以下题目：\n{test_question}"
            }
        ],
        temperature=0.3,
        max_tokens=500
    )

    answer = response.choices[0].message.content
    print("="*50)
    print("DeepSeek API连接成功！")
    print("="*50)
    print(f"\nAI回答:\n{answer}\n")
    print("="*50)
    print("测试完成！DeepSeek配置正常工作")
    print("="*50)

except Exception as e:
    print("="*50)
    print("API调用失败")
    print("="*50)
    print(f"错误信息: {e}")
    print("\n可能的原因:")
    print("1. API Key不正确")
    print("2. 网络连接问题")
    print("3. API配额不足")
    sys.exit(1)
