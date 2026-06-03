"""
测试脚本 - 测试各个模块功能
"""

import sys
from pathlib import Path

# 添加项目根目录到路径
ROOT_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT_DIR))


def test_imports():
    """测试模块导入"""
    print("=" * 50)
    print("测试模块导入...")
    print("=" * 50)

    try:
        import yaml
        print("✅ yaml")
    except ImportError as e:
        print(f"❌ yaml: {e}")

    try:
        from PIL import Image
        print("✅ PIL")
    except ImportError as e:
        print(f"❌ PIL: {e}")

    try:
        import mss
        print("✅ mss")
    except ImportError as e:
        print(f"❌ mss: {e}")

    try:
        import numpy
        print("✅ numpy")
    except ImportError as e:
        print(f"❌ numpy: {e}")

    try:
        import cv2
        print("✅ opencv")
    except ImportError as e:
        print(f"❌ opencv: {e}")

    try:
        import paddleocr
        print("✅ paddleocr")
    except ImportError as e:
        print(f"❌ paddleocr: {e}")

    try:
        import openai
        print("✅ openai")
    except ImportError as e:
        print(f"❌ openai: {e}")

    try:
        import keyboard
        print("✅ keyboard")
    except ImportError as e:
        print(f"❌ keyboard: {e}")

    print()


def test_config():
    """测试配置文件"""
    print("=" * 50)
    print("测试配置文件...")
    print("=" * 50)

    config_path = ROOT_DIR / "config" / "config.yaml"

    if not config_path.exists():
        print("❌ config.yaml 不存在")
        print("   请复制 config.example.yaml 为 config.yaml")
        return False

    try:
        import yaml
        with open(config_path, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)

        print("✅ 配置文件加载成功")

        # 检查必要配置
        if 'ai' not in config:
            print("❌ 缺少 ai 配置")
            return False

        if config['ai'].get('api_key') == 'your-api-key-here':
            print("⚠️  API密钥未配置")
        else:
            print("✅ API密钥已配置")

        print(f"   提供商: {config['ai'].get('provider')}")
        print(f"   模型: {config['ai'].get('model')}")

        return True

    except Exception as e:
        print(f"❌ 配置文件解析失败: {e}")
        return False

    print()


def test_ocr():
    """测试OCR模块"""
    print("=" * 50)
    print("测试OCR模块...")
    print("=" * 50)

    try:
        from src.ocr_engine import OCREngine
        from PIL import Image, ImageDraw, ImageFont

        print("⏳ 初始化OCR引擎（首次较慢）...")

        config = {
            'ocr': {
                'lang': 'ch_en',
                'use_gpu': False,
                'confidence_threshold': 0.5
            }
        }

        engine = OCREngine(config)
        print("✅ OCR引擎初始化成功")

        # 创建测试图片
        print("📝 创建测试图片...")
        img = Image.new('RGB', (400, 100), color='white')
        draw = ImageDraw.Draw(img)

        # 使用默认字体
        text = "测试文本 Test OCR 123"
        draw.text((10, 30), text, fill='black')

        print("🔍 开始识别...")
        result = engine.recognize(img)

        if result:
            print(f"✅ 识别结果: {result}")
        else:
            print("⚠️  未识别到文字")

        return True

    except Exception as e:
        print(f"❌ OCR测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

    print()


def test_screen_capture():
    """测试截图模块"""
    print("=" * 50)
    print("测试截图模块...")
    print("=" * 50)

    try:
        from src.screen_capture import ScreenCapture

        capture = ScreenCapture()
        print("✅ 截图模块加载成功")

        print("📸 测试全屏截图...")
        img = capture.capture_fullscreen()

        if img:
            print(f"✅ 全屏截图成功: {img.size}")
        else:
            print("❌ 全屏截图失败")
            return False

        return True

    except Exception as e:
        print(f"❌ 截图测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

    print()


def main():
    """运行所有测试"""
    print("\n🧪 AI自动答题系统 - 模块测试\n")

    # 测试导入
    test_imports()

    # 测试配置
    config_ok = test_config()
    print()

    # 测试截图
    test_screen_capture()
    print()

    # 测试OCR（可选，因为首次运行较慢）
    print("是否测试OCR模块？（首次运行会下载模型，较慢）")
    print("输入 y 继续，其他键跳过: ", end='')

    try:
        choice = input().strip().lower()
        if choice == 'y':
            test_ocr()
    except KeyboardInterrupt:
        print("\n\n测试中断")

    print("\n" + "=" * 50)
    print("测试完成！")
    print("=" * 50)

    if not config_ok:
        print("\n⚠️  请先配置 config/config.yaml 文件")


if __name__ == "__main__":
    main()
