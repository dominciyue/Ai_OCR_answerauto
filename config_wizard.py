"""
AI自动答题系统 - 首次启动配置向导
"""
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import yaml
from pathlib import Path
import sys
import io

# 设置UTF-8编码
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')


class ConfigWizard:
    """配置向导"""

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("AI自动答题系统 - 配置向导")
        self.root.geometry("700x600")
        self.root.resizable(False, False)

        # 居中显示
        self.center_window()

        # 配置数据
        self.config_data = {
            'ai_provider': 'deepseek',
            'ai_key': '',
            'ai_model': 'deepseek-chat',
            'ai_base_url': 'https://api.deepseek.com',
            'use_free_ocr': True,
            'baidu_api_key': '',
            'baidu_secret_key': '',
            'hotkey': 'f9'
        }

        self.create_widgets()

    def center_window(self):
        """窗口居中"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')

    def create_widgets(self):
        """创建界面"""
        # 标题
        title_frame = tk.Frame(self.root, bg='#4CAF50', height=80)
        title_frame.pack(fill='x')
        title_frame.pack_propagate(False)

        tk.Label(
            title_frame,
            text="🤖 AI自动答题系统",
            font=('Arial', 20, 'bold'),
            bg='#4CAF50',
            fg='white'
        ).pack(pady=20)

        # 主内容区
        main_frame = tk.Frame(self.root, padx=30, pady=20)
        main_frame.pack(fill='both', expand=True)

        # AI配置部分
        ai_frame = ttk.LabelFrame(main_frame, text="AI配置", padding=15)
        ai_frame.pack(fill='x', pady=(0, 15))

        # AI Provider
        tk.Label(ai_frame, text="AI提供商:", font=('Arial', 10)).grid(row=0, column=0, sticky='w', pady=5)
        self.ai_provider_var = tk.StringVar(value='deepseek')
        provider_combo = ttk.Combobox(
            ai_frame,
            textvariable=self.ai_provider_var,
            values=['deepseek', 'openai', 'claude'],
            state='readonly',
            width=25
        )
        provider_combo.grid(row=0, column=1, pady=5, sticky='ew')
        provider_combo.bind('<<ComboboxSelected>>', self.on_provider_change)

        # API Key
        tk.Label(ai_frame, text="API Key:", font=('Arial', 10)).grid(row=1, column=0, sticky='w', pady=5)
        self.ai_key_entry = tk.Entry(ai_frame, width=30, font=('Arial', 9))
        self.ai_key_entry.grid(row=1, column=1, pady=5, sticky='ew')

        # 模型
        tk.Label(ai_frame, text="模型:", font=('Arial', 10)).grid(row=2, column=0, sticky='w', pady=5)
        self.ai_model_var = tk.StringVar(value='deepseek-chat')
        self.ai_model_entry = tk.Entry(ai_frame, textvariable=self.ai_model_var, width=30, font=('Arial', 9))
        self.ai_model_entry.grid(row=2, column=1, pady=5, sticky='ew')

        ai_frame.columnconfigure(1, weight=1)

        # OCR配置部分
        ocr_frame = ttk.LabelFrame(main_frame, text="OCR配置", padding=15)
        ocr_frame.pack(fill='x', pady=(0, 15))

        self.use_free_ocr_var = tk.BooleanVar(value=True)
        tk.Checkbutton(
            ocr_frame,
            text="使用免费OCR（无需配置，推荐）",
            variable=self.use_free_ocr_var,
            font=('Arial', 10),
            command=self.on_ocr_mode_change
        ).pack(anchor='w')

        self.baidu_frame = tk.Frame(ocr_frame)
        self.baidu_frame.pack(fill='x', pady=(10, 0))

        tk.Label(self.baidu_frame, text="百度API Key:", font=('Arial', 9), fg='gray').grid(row=0, column=0, sticky='w', pady=3)
        self.baidu_key_entry = tk.Entry(self.baidu_frame, width=30, font=('Arial', 9), state='disabled')
        self.baidu_key_entry.grid(row=0, column=1, pady=3, sticky='ew')

        tk.Label(self.baidu_frame, text="百度Secret Key:", font=('Arial', 9), fg='gray').grid(row=1, column=0, sticky='w', pady=3)
        self.baidu_secret_entry = tk.Entry(self.baidu_frame, width=30, font=('Arial', 9), state='disabled')
        self.baidu_secret_entry.grid(row=1, column=1, pady=3, sticky='ew')

        self.baidu_frame.columnconfigure(1, weight=1)

        # 快捷键配置
        hotkey_frame = ttk.LabelFrame(main_frame, text="快捷键设置", padding=15)
        hotkey_frame.pack(fill='x', pady=(0, 15))

        tk.Label(hotkey_frame, text="启动快捷键:", font=('Arial', 10)).grid(row=0, column=0, sticky='w', pady=5)
        self.hotkey_var = tk.StringVar(value='f9')
        hotkey_entry = tk.Entry(hotkey_frame, textvariable=self.hotkey_var, width=10, font=('Arial', 10))
        hotkey_entry.grid(row=0, column=1, pady=5)
        tk.Label(hotkey_frame, text="（默认: F9）", font=('Arial', 9), fg='gray').grid(row=0, column=2, sticky='w', padx=(10, 0))

        # 按钮区
        button_frame = tk.Frame(main_frame)
        button_frame.pack(fill='x', pady=(10, 0))

        tk.Button(
            button_frame,
            text="保存配置并启动",
            command=self.save_and_start,
            bg='#4CAF50',
            fg='white',
            font=('Arial', 11, 'bold'),
            padx=20,
            pady=8,
            relief='flat',
            cursor='hand2'
        ).pack(side='right', padx=(5, 0))

        tk.Button(
            button_frame,
            text="取消",
            command=self.root.quit,
            bg='#757575',
            fg='white',
            font=('Arial', 11),
            padx=20,
            pady=8,
            relief='flat',
            cursor='hand2'
        ).pack(side='right')

    def on_provider_change(self, event=None):
        """AI提供商变更"""
        provider = self.ai_provider_var.get()

        if provider == 'deepseek':
            self.ai_model_var.set('deepseek-chat')
        elif provider == 'openai':
            self.ai_model_var.set('gpt-4o')
        elif provider == 'claude':
            self.ai_model_var.set('claude-3-5-sonnet-20241022')

    def on_ocr_mode_change(self):
        """OCR模式变更"""
        use_free = self.use_free_ocr_var.get()
        state = 'disabled' if use_free else 'normal'

        self.baidu_key_entry.config(state=state)
        self.baidu_secret_entry.config(state=state)

    def save_and_start(self):
        """保存配置并启动"""
        # 验证AI配置
        api_key = self.ai_key_entry.get().strip()
        if not api_key:
            messagebox.showerror("错误", "请填入AI API Key！")
            return

        # 验证百度OCR配置（如果需要）
        if not self.use_free_ocr_var.get():
            baidu_key = self.baidu_key_entry.get().strip()
            baidu_secret = self.baidu_secret_entry.get().strip()
            if not baidu_key or not baidu_secret:
                messagebox.showerror("错误", "请填入百度OCR的API Key和Secret Key！")
                return

        # 构建配置
        provider = self.ai_provider_var.get()
        base_url_map = {
            'deepseek': 'https://api.deepseek.com',
            'openai': None,
            'claude': None
        }

        config = {
            'ai': {
                'provider': 'openai' if provider in ['deepseek', 'openai'] else provider,
                'api_key': api_key,
                'model': self.ai_model_var.get(),
                'base_url': base_url_map[provider],
                'timeout': 30,
                'max_retries': 3
            },
            'ocr': {
                'use_free_api': self.use_free_ocr_var.get(),
                'baidu_api_key': self.baidu_key_entry.get().strip() if not self.use_free_ocr_var.get() else '',
                'baidu_secret_key': self.baidu_secret_entry.get().strip() if not self.use_free_ocr_var.get() else '',
                'confidence_threshold': 0.5
            },
            'gui': {
                'hotkey': self.hotkey_var.get(),
                'quit_hotkey': 'ctrl+q',
                'window_opacity': 0.95,
                'auto_close_seconds': 0,
                'theme': 'light'
            },
            'capture': {
                'save_screenshot': False,
                'screenshot_dir': './screenshots',
                'border_color': [255, 0, 0],
                'border_width': 2
            },
            'logging': {
                'level': 'INFO',
                'save_to_file': True,
                'log_file': './logs/app.log'
            }
        }

        # 保存配置
        try:
            config_path = Path('config/config.yaml')
            config_path.parent.mkdir(exist_ok=True)

            with open(config_path, 'w', encoding='utf-8') as f:
                yaml.dump(config, f, allow_unicode=True, default_flow_style=False)

            messagebox.showinfo("成功", "配置已保存！\n\n程序即将启动...")
            self.root.quit()

            # 启动主程序
            import subprocess
            subprocess.Popen([sys.executable, 'src/main.py'])

        except Exception as e:
            messagebox.showerror("错误", f"保存配置失败: {e}")

    def run(self):
        """运行向导"""
        self.root.mainloop()


if __name__ == "__main__":
    wizard = ConfigWizard()
    wizard.run()
