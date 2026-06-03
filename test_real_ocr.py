"""
完整流程测试 - 使用真实的RapidOCR
测试：截图 → RapidOCR识别 → AI回答
"""
import sys
import yaml
import io
from pathlib import Path

# 设置UTF-8编码输出
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from src.screen_capture import ScreenCapture
from src.ocr_engine import OCREngine
from src.ai_client import AIClient

def load_config():
    """加载配置文件"""
    config_path = Path("config/config.yaml")
    with open(config_path, 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f)
    return config

def main():
    print("=" * 60)
    print("AI自动答题系统 - 真实OCR完整流程测试")
    print("=" * 60)

    # 加载配置
    config = load_config()
    print(f"\n配置信息:")
    print(f"  AI提供商: {config['ai']['provider']}")
    print(f"  模型: {config['ai']['model']}")
    print(f"  OCR引擎: RapidOCR (离线)")

    # 初始化模块
    print("\n正在初始化模块...")
    screen_capture = ScreenCapture(config)

    print("正在初始化OCR引擎（首次启动会下载模型，请稍候）...")
    ocr_engine = OCREngine(config)

    ai_client = AIClient(config)
    print("✅ 所有模块初始化成功！")

    print("\n" + "=" * 60)
    print("请按任意键开始截图测试...")
    print("提示：请截取包含题目文字的区域")
    print("=" * 60)
    input()

    # 测试截图
    print("\n正在启动截图...")

    def on_capture_done(image, selection):
        print("\n回调函数被调用...")

        if image is None:
            print("❌ 截图已取消")
            import sys
            sys.exit(0)

        print(f"✅ 截图成功: {image.size}")

        # 真实OCR识别
        print("\n正在进行OCR识别（RapidOCR）...")
        print("这可能需要几秒钟，请稍候...")

        try:
            question_text = ocr_engine.recognize(image)

            if not question_text or not question_text.strip():
                print("❌ OCR未识别到文字，请重新截取包含文字的区域")
                import sys
                sys.exit(0)

            print(f"✅ OCR识别完成!")
            print("\n识别的文字:")
            print("-" * 60)
            print(question_text)
            print("-" * 60)

            # AI问答
            print("\n正在请求AI回答...")
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
            print(f"\n❌ 处理错误: {e}")
            import traceback
            traceback.print_exc()

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
