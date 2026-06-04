"""
AI自动答题系统 - 主程序（修复打包问题）
"""

import sys
import logging
import yaml
from pathlib import Path
import io

# 设置UTF-8编码输出（仅在有控制台时）
try:
    if sys.stdout is not None and hasattr(sys.stdout, 'buffer') and sys.stdout.buffer is not None:
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    if sys.stderr is not None and hasattr(sys.stderr, 'buffer') and sys.stderr.buffer is not None:
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')
except:
    pass  # 打包后windowed模式下忽略

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

    # 如果不存在，显示首次配置向导
    if not config_path.exists():
        example_path = ROOT_DIR / "config" / "config.example.yaml"

        # 如果example也不存在，创建一个
        if not example_path.exists():
            example_path.parent.mkdir(parents=True, exist_ok=True)
            # 创建最小配置
            example_config = {
                "ai": {"provider": "openai", "api_key": "your-api-key-here", "model": "deepseek-chat", "base_url": "https://api.deepseek.com"},
                "ocr": {"confidence_threshold": 0.5},
                "gui": {"hotkey": "f9", "quit_hotkey": "ctrl+q"},
                "capture": {"border_color": [255, 0, 0], "border_width": 2},
                "logging": {"level": "INFO", "save_to_file": True, "log_file": "./logs/app.log"}
            }
            with open(example_path, 'w', encoding='utf-8') as f:
                yaml.dump(example_config, f, allow_unicode=True, default_flow_style=False)

        # 显示配置向导
        try:
            from src.config_wizard import show_first_run_wizard
            config = show_first_run_wizard(config_path)
            if config:
                return config
            else:
                # 用户跳过，退出
                sys.exit(0)
        except Exception as e:
            import tkinter as tk
            from tkinter import messagebox
            root = tk.Tk()
            root.withdraw()
            messagebox.showerror("错误", f"配置向导启动失败:\n\n{e}")
            sys.exit(1)

    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
        return config
    except Exception as e:
        import tkinter as tk
        from tkinter import messagebox
        root = tk.Tk()
        root.withdraw()
        messagebox.showerror("配置文件错误", f"配置文件加载失败:\n\n{e}")
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
        import tkinter as tk
        from tkinter import messagebox
        root = tk.Tk()
        root.withdraw()
        messagebox.showerror(
            "API密钥未配置",
            "请在 config/config.yaml 中配置有效的API密钥！\n\n"
            "参考: config/config.example.yaml 或 CONFIG_GUIDE.md"
        )
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
        import tkinter as tk
        from tkinter import messagebox
        root = tk.Tk()
        root.withdraw()
        messagebox.showerror("程序错误", f"程序运行出错:\n\n{e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
