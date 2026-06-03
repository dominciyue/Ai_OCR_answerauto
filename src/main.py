"""
AI自动答题系统 - 主程序
"""

import os
import sys
import logging
import yaml
from pathlib import Path
import io

# 设置UTF-8编码输出
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# 添加项目根目录到路径
ROOT_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT_DIR))

from src.gui import AnswerSystemGUI


def load_config():
    """加载配置文件"""
    config_path = ROOT_DIR / "config" / "config.yaml"

    if not config_path.exists():
        print("❌ 配置文件不存在！")
        print(f"请复制 config/config.example.yaml 为 config/config.yaml 并填入API密钥")
        sys.exit(1)

    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
        return config
    except Exception as e:
        print(f"❌ 配置文件加载失败: {e}")
        sys.exit(1)


def setup_logging(config):
    """设置日志"""
    log_level = config.get('logging', {}).get('level', 'INFO')
    save_to_file = config.get('logging', {}).get('save_to_file', False)

    # 基础配置
    log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    handlers = [logging.StreamHandler()]

    # 如果需要保存到文件
    if save_to_file:
        log_file = Path(config.get('logging', {}).get('log_file', './logs/app.log'))
        log_file.parent.mkdir(parents=True, exist_ok=True)
        handlers.append(logging.FileHandler(log_file, encoding='utf-8'))

    logging.basicConfig(
        level=getattr(logging, log_level),
        format=log_format,
        handlers=handlers
    )


def main():
    """主函数"""
    print("=" * 50)
    print("🚀 AI自动答题系统")
    print("=" * 50)

    # 加载配置
    print("📋 正在加载配置...")
    config = load_config()

    # 设置日志
    setup_logging(config)
    logger = logging.getLogger(__name__)

    # 验证API密钥
    api_key = config.get('ai', {}).get('api_key')
    if not api_key or api_key == "your-api-key-here":
        print("❌ 请在 config/config.yaml 中配置有效的API密钥！")
        sys.exit(1)

    logger.info("配置加载成功")

    # 创建截图目录
    if config.get('capture', {}).get('save_screenshot', False):
        screenshot_dir = Path(config['capture']['screenshot_dir'])
        screenshot_dir.mkdir(parents=True, exist_ok=True)
        logger.info(f"截图保存目录: {screenshot_dir}")

    print("✅ 配置加载完成")
    print(f"🤖 AI提供商: {config['ai']['provider']}")
    print(f"📦 模型: {config['ai']['model']}")
    print(f"⌨️  快捷键: {config['gui']['hotkey'].upper()}")
    print("=" * 50)
    print("\n按下快捷键开始使用！\n")

    # 启动GUI
    try:
        app = AnswerSystemGUI(config)
        app.run()
    except KeyboardInterrupt:
        logger.info("用户中断程序")
        print("\n👋 程序已退出")
    except Exception as e:
        logger.error(f"程序运行出错: {e}", exc_info=True)
        print(f"\n❌ 程序出错: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
