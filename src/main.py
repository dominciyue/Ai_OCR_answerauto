"""
AI自动答题系统 - 主程序（修复打包问题）
"""

import os
import sys
import logging
import yaml
from pathlib import Path
import io

# 设置UTF-8编码输出（仅在有控制台时）
if sys.stdout is not None and hasattr(sys.stdout, 'buffer') and sys.stdout.buffer is not None:
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
if sys.stderr is not None and hasattr(sys.stderr, 'buffer') and sys.stderr.buffer is not None:
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# 判断是否打包运行
if getattr(sys, 'frozen', False):
    # 打包后的exe运行
    ROOT_DIR = Path(sys.executable).parent
else:
    # 开发环境运行
    ROOT_DIR = Path(__file__).parent.parent

sys.path.insert(0, str(ROOT_DIR))

from src.gui import AnswerSystemGUI


def load_config():
    """加载配置文件"""
    config_path = ROOT_DIR / "config" / "config.yaml"

    # 如果不存在，尝试从example复制
    if not config_path.exists():
        example_path = ROOT_DIR / "config" / "config.example.yaml"
        if example_path.exists():
            print("⚠️  首次运行，正在创建配置文件...")
            config_path.parent.mkdir(parents=True, exist_ok=True)
            import shutil
            shutil.copy(example_path, config_path)
            print("✅ 配置文件已创建")

    if not config_path.exists():
        print("❌ 配置文件不存在！")
        print(f"请在程序目录下创建 config/config.yaml 配置文件")
        print(f"参考: config/config.example.yaml")
        input("按回车键退出...")
        sys.exit(1)

    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
        return config
    except Exception as e:
        print(f"❌ 配置文件加载失败: {e}")
        input("按回车键退出...")
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
        log_file = ROOT_DIR / Path(config.get('logging', {}).get('log_file', './logs/app.log'))
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
    if not api_key or api_key in ["your-api-key-here", "your-deepseek-api-key-here"]:
        print("❌ 请在 config/config.yaml 中配置有效的API密钥！")
        print("📖 参考: config/config.example.yaml 或 CONFIG_GUIDE.md")
        input("按回车键退出...")
        sys.exit(1)

    logger.info("配置加载成功")

    # 创建必要的目录
    data_dir = ROOT_DIR / "data"
    data_dir.mkdir(parents=True, exist_ok=True)

    logs_dir = ROOT_DIR / "logs"
    logs_dir.mkdir(parents=True, exist_ok=True)

    # 创建截图目录
    if config.get('capture', {}).get('save_screenshot', False):
        screenshot_dir = ROOT_DIR / Path(config['capture']['screenshot_dir'])
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
        input("按回车键退出...")
        sys.exit(1)


if __name__ == "__main__":
    main()
