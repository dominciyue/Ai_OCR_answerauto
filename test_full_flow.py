"""
完整流程测试 - 使用模拟OCR
测试：截图 → 模拟OCR → AI回答
"""
import sys
import yaml
import io
from pathlib import Path

# 设置UTF-8编码输出
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from src.screen_capture import ScreenCapture
from src.ai_client import AIClient

def load_config():
    """加载配置文件"""
    config_path = Path("config/config.yaml")
    with open(config_path, 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f)
    return config

def mock_ocr(image):
    """模拟OCR - 返回测试题目"""
    return """
以下哪项是Python的特点？
A. 静态类型
B. 动态类型
C. 编译型语言
D. 不支持面向对象
"""

def main():
    print("=" * 60)
    print("AI自动答题系统 - 完整流程测试")
    print("=" * 60)

    # 加载配置
    config = load_config()
    print(f"\n配置信息:")
    print(f"  AI提供商: {config['ai']['provider']}")
    print(f"  模型: {config['ai']['model']}")

    # 初始化模块
    print("\n正在初始化模块...")
    screen_capture = ScreenCapture(config)
    ai_client = AIClient(config)
    print("✅ 模块初始化成功！")

    print("\n" + "=" * 60)
    print("请按任意键开始截图测试...")
    print("=" * 60)
    input()

    # 测试截图
    print("\n正在启动截图...")
    print("提示：截图窗口会全屏显示，用鼠标拖动选择区域")
    print("      按ESC可以取消\n")

    def on_capture_done(image, selection):
        print("\n回调函数被调用...")

        if image is None:
            print("❌ 截图已取消")
            import sys
            sys.exit(0)

        print(f"✅ 截图成功: {image.size}")

        # 模拟OCR识别
        print("\n正在进行OCR识别（模拟）...")
        question_text = mock_ocr(image)
        print(f"✅ OCR识别完成:")
        print(question_text)

        # AI问答
        print("\n正在请求AI回答...")
        try:
            answer = ai_client.answer_question(question_text)
            if answer:
                print("\n" + "=" * 60)
                print("✅ AI回答:")
                print("=" * 60)
                print(answer)
                print("=" * 60)
                print("\n✨ 完整流程测试成功！")
            else:
                print("\n❌ AI回答失败")
        except Exception as e:
            print(f"\n❌ AI调用错误: {e}")

        import sys
        sys.exit(0)

    try:
        # 执行交互式截图
        screen_capture.capture_region_interactive(on_capture_done)
    except Exception as e:
        print(f"\n❌ 截图失败: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
