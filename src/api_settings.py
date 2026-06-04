"""
API配置设置窗口
"""
import tkinter as tk
from tkinter import messagebox
import yaml
from pathlib import Path


class APISettings:
    """API配置设置窗口"""

    def __init__(self, parent, config_path):
        self.parent = parent
        self.config_path = Path(config_path)
        self.result = None

        self.window = tk.Toplevel(parent)
        self.window.title("API配置")
        self.window.geometry("600x450")
        self.window.transient(parent)
        self.window.grab_set()

        # 加载当前配置
        self._load_config()
        self._create_widgets()
        self._center_window()

    def _load_config(self):
        """加载当前配置"""
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                self.config = yaml.safe_load(f)
        except:
            self.config = {}

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
        title_frame = tk.Frame(self.window, bg='#2196F3', height=60)
        title_frame.pack(fill='x')
        title_frame.pack_propagate(False)

        tk.Label(
            title_frame,
            text="⚙️ API配置",
            font=('Microsoft YaHei UI', 14, 'bold'),
            bg='#2196F3',
            fg='white'
        ).pack(pady=15)

        # 主内容
        main_frame = tk.Frame(self.window, padx=30, pady=20)
        main_frame.pack(fill='both', expand=True)

        # AI提供商
        tk.Label(
            main_frame,
            text="AI提供商：",
            font=('Microsoft YaHei UI', 10)
        ).grid(row=0, column=0, sticky='w', pady=10)

        self.provider_var = tk.StringVar()
        current_model = self.config.get('ai', {}).get('model', 'deepseek-chat')

        # 根据模型判断当前提供商
        if 'deepseek' in current_model:
            self.provider_var.set('DeepSeek')
        elif 'qwen' in current_model:
            self.provider_var.set('通义千问')
        elif 'glm' in current_model:
            self.provider_var.set('智谱AI')
        elif 'moonshot' in current_model:
            self.provider_var.set('Moonshot')
        elif 'Baichuan' in current_model:
            self.provider_var.set('百川智能')
        elif 'gpt' in current_model:
            self.provider_var.set('OpenAI GPT')
        elif 'claude' in current_model:
            self.provider_var.set('Claude')
        else:
            self.provider_var.set('DeepSeek')

        tk.Entry(
            main_frame,
            textvariable=self.provider_var,
            font=('Microsoft YaHei UI', 10),
            width=30,
            state='readonly'
        ).grid(row=0, column=1, pady=10, sticky='w')

        # API密钥
        tk.Label(
            main_frame,
            text="API密钥：",
            font=('Microsoft YaHei UI', 10)
        ).grid(row=1, column=0, sticky='w', pady=10)

        self.api_key_var = tk.StringVar(value=self.config.get('ai', {}).get('api_key', ''))
        self.api_key_entry = tk.Entry(
            main_frame,
            textvariable=self.api_key_var,
            font=('Microsoft YaHei UI', 10),
            width=40,
            show='*'
        )
        self.api_key_entry.grid(row=1, column=1, pady=10, sticky='w')

        # 显示/隐藏密钥
        self.show_key_var = tk.BooleanVar()
        tk.Checkbutton(
            main_frame,
            text="显示密钥",
            variable=self.show_key_var,
            command=self._toggle_key_visibility
        ).grid(row=2, column=1, sticky='w')

        # 模型
        tk.Label(
            main_frame,
            text="模型：",
            font=('Microsoft YaHei UI', 10)
        ).grid(row=3, column=0, sticky='w', pady=10)

        tk.Label(
            main_frame,
            text=current_model,
            font=('Microsoft YaHei UI', 10),
            fg='#666'
        ).grid(row=3, column=1, sticky='w', pady=10)

        # 提示
        tk.Label(
            main_frame,
            text="提示：修改配置后需要重启程序生效",
            font=('Microsoft YaHei UI', 9),
            fg='#f44336'
        ).grid(row=4, column=0, columnspan=2, sticky='w', pady=20)

        # 按钮
        button_frame = tk.Frame(main_frame)
        button_frame.grid(row=5, column=0, columnspan=2, pady=10)

        tk.Button(
            button_frame,
            text="保存",
            command=self._save,
            bg='#4CAF50',
            fg='white',
            font=('Microsoft YaHei UI', 10),
            padx=30,
            pady=8,
            relief='flat',
            cursor='hand2'
        ).pack(side='left', padx=5)

        tk.Button(
            button_frame,
            text="取消",
            command=self.window.destroy,
            bg='#757575',
            fg='white',
            font=('Microsoft YaHei UI', 10),
            padx=30,
            pady=8,
            relief='flat',
            cursor='hand2'
        ).pack(side='left', padx=5)

    def _toggle_key_visibility(self):
        """切换密钥显示"""
        if self.show_key_var.get():
            self.api_key_entry.config(show='')
        else:
            self.api_key_entry.config(show='*')

    def _save(self):
        """保存配置"""
        api_key = self.api_key_var.get().strip()

        if not api_key:
            messagebox.showerror("错误", "API密钥不能为空！", parent=self.window)
            return

        try:
            # 更新配置
            self.config['ai']['api_key'] = api_key

            # 保存到文件
            with open(self.config_path, 'w', encoding='utf-8') as f:
                yaml.dump(self.config, f, allow_unicode=True, default_flow_style=False)

            messagebox.showinfo(
                "成功",
                "配置已保存！\n\n请重启程序使配置生效。",
                parent=self.window
            )
            self.result = True
            self.window.destroy()

        except Exception as e:
            messagebox.showerror("错误", f"保存失败:\n\n{e}", parent=self.window)


def show_api_settings(parent, config_path):
    """显示API配置对话框"""
    dialog = APISettings(parent, config_path)
    parent.wait_window(dialog.window)
    return dialog.result
