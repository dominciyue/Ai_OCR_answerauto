"""
首次运行配置向导 - 修复版
"""
import tkinter as tk
from tkinter import messagebox
import yaml
from pathlib import Path


class FirstRunWizard:
    """首次运行配置向导"""

    def __init__(self, config_path):
        self.config_path = Path(config_path)
        self.config = None
        self.saved = False

        self.window = tk.Tk()
        self.window.title("AI答题系统 - 首次配置")
        self.window.geometry("600x650")  # 增加高度
        self.window.resizable(False, False)

        # 窗口关闭事件
        self.window.protocol("WM_DELETE_WINDOW", self._on_close)

        # 居中显示
        self._center_window()

        # 创建界面
        self._create_widgets()

    def _center_window(self):
        """窗口居中"""
        self.window.update_idletasks()
        width = self.window.winfo_width()
        height = self.window.winfo_height()
        x = (self.window.winfo_screenwidth() // 2) - (width // 2)
        y = (self.window.winfo_screenheight() // 2) - (height // 2)
        self.window.geometry(f'{width}x{height}+{x}+{y}')

    def _create_widgets(self):
        """创建界面"""
        # 标题
        title_frame = tk.Frame(self.window, bg='#4CAF50', height=80)
        title_frame.pack(fill='x')
        title_frame.pack_propagate(False)

        tk.Label(
            title_frame,
            text="🚀 欢迎使用AI答题系统",
            font=('Microsoft YaHei UI', 16, 'bold'),
            bg='#4CAF50',
            fg='white'
        ).pack(pady=10)

        tk.Label(
            title_frame,
            text="首次运行需要配置API密钥",
            font=('Microsoft YaHei UI', 10),
            bg='#4CAF50',
            fg='white'
        ).pack()

        # 主内容
        main_frame = tk.Frame(self.window, padx=30, pady=20)
        main_frame.pack(fill='both', expand=True)

        # AI提供商选择
        tk.Label(
            main_frame,
            text="选择AI提供商：",
            font=('Microsoft YaHei UI', 11, 'bold')
        ).grid(row=0, column=0, sticky='w', pady=(0, 10))

        self.provider_var = tk.StringVar(value="deepseek")

        providers = [
            ("DeepSeek（推荐 - 性价比最高）", "deepseek"),
            ("通义千问（阿里云）", "qwen"),
            ("智谱AI（清华）", "zhipu"),
            ("Moonshot（Kimi）", "moonshot"),
            ("百川智能", "baichuan"),
            ("OpenAI GPT", "openai"),
        ]

        for i, (label, value) in enumerate(providers):
            tk.Radiobutton(
                main_frame,
                text=label,
                variable=self.provider_var,
                value=value,
                font=('Microsoft YaHei UI', 10),
                command=self._on_provider_change
            ).grid(row=i+1, column=0, sticky='w', padx=20)

        # API密钥输入
        tk.Label(
            main_frame,
            text="API密钥：",
            font=('Microsoft YaHei UI', 11, 'bold')
        ).grid(row=len(providers)+1, column=0, sticky='w', pady=(20, 5))

        self.api_key_var = tk.StringVar()
        self.api_key_entry = tk.Entry(
            main_frame,
            textvariable=self.api_key_var,
            font=('Microsoft YaHei UI', 10),
            width=50,
            show='*'
        )
        self.api_key_entry.grid(row=len(providers)+2, column=0, pady=5, sticky='w')

        # 显示/隐藏密钥
        self.show_key_var = tk.BooleanVar()
        tk.Checkbutton(
            main_frame,
            text="显示密钥",
            variable=self.show_key_var,
            command=self._toggle_key_visibility
        ).grid(row=len(providers)+3, column=0, sticky='w', pady=5)

        # 提示信息
        self.hint_label = tk.Label(
            main_frame,
            text="",
            font=('Microsoft YaHei UI', 9),
            fg='#666',
            wraplength=500,
            justify='left'
        )
        self.hint_label.grid(row=len(providers)+4, column=0, sticky='w', pady=10)

        # 更新提示
        self._on_provider_change()

        # 按钮
        button_frame = tk.Frame(main_frame)
        button_frame.grid(row=len(providers)+5, column=0, pady=20)

        tk.Button(
            button_frame,
            text="保存并启动",
            command=self._save_and_start,
            bg='#4CAF50',
            fg='white',
            font=('Microsoft YaHei UI', 11, 'bold'),
            padx=30,
            pady=10,
            relief='flat',
            cursor='hand2'
        ).pack(side='left', padx=5)

    def _on_provider_change(self):
        """提供商改变时更新提示"""
        provider = self.provider_var.get()

        hints = {
            "deepseek": "🌟 推荐！\n• 注册：https://platform.deepseek.com/\n• 新用户送500万tokens\n• 1000题≈¥1",
            "qwen": "• 注册：https://dashscope.aliyun.com/\n• 阿里云出品，速度快",
            "zhipu": "• 注册：https://open.bigmodel.cn/\n• 清华出品，效果好",
            "moonshot": "• 注册：https://platform.moonshot.cn/\n• Kimi出品，上下文长",
            "baichuan": "• 注册：https://platform.baichuan-ai.com/\n• 百川出品，性能稳定",
            "openai": "• 注册：https://platform.openai.com/\n• 需要翻墙",
        }

        self.hint_label.config(text=hints.get(provider, ""))

    def _toggle_key_visibility(self):
        """切换密钥显示/隐藏"""
        if self.show_key_var.get():
            self.api_key_entry.config(show='')
        else:
            self.api_key_entry.config(show='*')

    def _save_and_start(self):
        """保存配置并启动"""
        api_key = self.api_key_var.get().strip()

        if not api_key:
            messagebox.showerror("错误", "请输入API密钥！", parent=self.window)
            return

        provider = self.provider_var.get()

        # 配置映射
        config_map = {
            "deepseek": {
                "provider": "openai",
                "model": "deepseek-chat",
                "base_url": "https://api.deepseek.com"
            },
            "qwen": {
                "provider": "openai",
                "model": "qwen-turbo",
                "base_url": "https://dashscope.aliyuncs.com/compatible-mode/v1"
            },
            "zhipu": {
                "provider": "openai",
                "model": "glm-4-flash",
                "base_url": "https://open.bigmodel.cn/api/paas/v4"
            },
            "moonshot": {
                "provider": "openai",
                "model": "moonshot-v1-8k",
                "base_url": "https://api.moonshot.cn/v1"
            },
            "baichuan": {
                "provider": "openai",
                "model": "Baichuan2-Turbo",
                "base_url": "https://api.baichuan-ai.com/v1"
            },
            "openai": {
                "provider": "openai",
                "model": "gpt-4o",
                "base_url": None
            },
        }

        provider_config = config_map[provider]

        # 创建完整配置
        self.config = {
            "ai": {
                "provider": provider_config["provider"],
                "api_key": api_key,
                "model": provider_config["model"],
                "base_url": provider_config["base_url"],
                "timeout": 30,
                "max_retries": 3
            },
            "ocr": {
                "confidence_threshold": 0.5
            },
            "gui": {
                "hotkey": "f9",
                "quit_hotkey": "ctrl+q",
                "window_opacity": 0.95,
                "auto_close_seconds": 0,
                "theme": "light",
                "enable_tray": False
            },
            "capture": {
                "save_screenshot": False,
                "screenshot_dir": "./screenshots",
                "border_color": [255, 0, 0],
                "border_width": 2
            },
            "logging": {
                "level": "INFO",
                "save_to_file": True,
                "log_file": "./logs/app.log"
            }
        }

        # 保存到文件
        try:
            self.config_path.parent.mkdir(parents=True, exist_ok=True)
            with open(self.config_path, 'w', encoding='utf-8') as f:
                yaml.dump(self.config, f, allow_unicode=True, default_flow_style=False)

            self.saved = True
            self.window.destroy()

        except Exception as e:
            messagebox.showerror("错误", f"保存配置失败:\n\n{e}", parent=self.window)

    def _on_close(self):
        """窗口关闭事件"""
        if not self.saved:
            result = messagebox.askyesno(
                "确认退出",
                "配置尚未保存，确定要退出吗？\n\n退出后无法使用程序。",
                parent=self.window
            )
            if result:
                self.window.destroy()
        else:
            self.window.destroy()

    def run(self):
        """显示向导并等待结果"""
        self.window.mainloop()
        return self.config if self.saved else None


def show_first_run_wizard(config_path):
    """显示首次运行向导"""
    wizard = FirstRunWizard(config_path)
    return wizard.run()
