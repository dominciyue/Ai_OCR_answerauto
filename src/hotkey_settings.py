"""
快捷键设置窗口
"""
import tkinter as tk
from tkinter import messagebox
import yaml
from pathlib import Path


class HotkeySettings:
    """快捷键设置窗口"""

    def __init__(self, parent, config):
        self.parent = parent
        self.config = config
        self.result = None

        self.window = tk.Toplevel(parent)
        self.window.title("快捷键设置")
        self.window.geometry("500x350")
        self.window.transient(parent)
        self.window.grab_set()

        self._create_widgets()
        self._center_window()

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
        title_frame = tk.Frame(self.window, bg='#4CAF50', height=60)
        title_frame.pack(fill='x')
        title_frame.pack_propagate(False)

        tk.Label(
            title_frame,
            text="⌨️ 快捷键设置",
            font=('Microsoft YaHei UI', 16, 'bold'),
            bg='#4CAF50',
            fg='white'
        ).pack(pady=15)

        # 主内容
        main_frame = tk.Frame(self.window, padx=30, pady=20)
        main_frame.pack(fill='both', expand=True)

        # 快速答题快捷键
        tk.Label(
            main_frame,
            text="快速答题快捷键：",
            font=('Microsoft YaHei UI', 11)
        ).grid(row=0, column=0, sticky='w', pady=10)

        self.hotkey_var = tk.StringVar(value=self.config.get('gui', {}).get('hotkey', 'f9'))
        hotkey_entry = tk.Entry(
            main_frame,
            textvariable=self.hotkey_var,
            font=('Microsoft YaHei UI', 10),
            width=20
        )
        hotkey_entry.grid(row=0, column=1, pady=10, padx=10)

        tk.Label(
            main_frame,
            text="(如: f9, f10, ctrl+shift+a)",
            font=('Microsoft YaHei UI', 9),
            fg='gray'
        ).grid(row=0, column=2, sticky='w')

        # 退出快捷键
        tk.Label(
            main_frame,
            text="退出程序快捷键：",
            font=('Microsoft YaHei UI', 11)
        ).grid(row=1, column=0, sticky='w', pady=10)

        self.quit_hotkey_var = tk.StringVar(value=self.config.get('gui', {}).get('quit_hotkey', 'ctrl+q'))
        quit_entry = tk.Entry(
            main_frame,
            textvariable=self.quit_hotkey_var,
            font=('Microsoft YaHei UI', 10),
            width=20
        )
        quit_entry.grid(row=1, column=1, pady=10, padx=10)

        tk.Label(
            main_frame,
            text="(如: ctrl+q, ctrl+shift+q)",
            font=('Microsoft YaHei UI', 9),
            fg='gray'
        ).grid(row=1, column=2, sticky='w')

        # 说明
        info_text = """
提示：
• 避免与系统或其他软件冲突
• 建议使用F10、F11等功能键
• 或使用组合键如 ctrl+shift+字母
• 修改后需要重启程序生效
        """
        tk.Label(
            main_frame,
            text=info_text,
            font=('Microsoft YaHei UI', 9),
            fg='#666',
            justify='left'
        ).grid(row=2, column=0, columnspan=3, sticky='w', pady=20)

        # 按钮
        button_frame = tk.Frame(main_frame)
        button_frame.grid(row=3, column=0, columnspan=3, pady=10)

        tk.Button(
            button_frame,
            text="保存",
            command=self.save,
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

    def save(self):
        """保存设置"""
        hotkey = self.hotkey_var.get().strip().lower()
        quit_hotkey = self.quit_hotkey_var.get().strip().lower()

        if not hotkey or not quit_hotkey:
            messagebox.showerror("错误", "快捷键不能为空！", parent=self.window)
            return

        if hotkey == quit_hotkey:
            messagebox.showerror("错误", "两个快捷键不能相同！", parent=self.window)
            return

        # 保存到配置文件
        try:
            config_path = Path("config/config.yaml")
            with open(config_path, 'r', encoding='utf-8') as f:
                config = yaml.safe_load(f)

            config['gui']['hotkey'] = hotkey
            config['gui']['quit_hotkey'] = quit_hotkey

            with open(config_path, 'w', encoding='utf-8') as f:
                yaml.dump(config, f, allow_unicode=True, default_flow_style=False)

            messagebox.showinfo(
                "成功",
                f"快捷键已保存！\n\n快速答题: {hotkey.upper()}\n退出程序: {quit_hotkey.upper()}\n\n请重启程序使设置生效。",
                parent=self.window
            )
            self.result = (hotkey, quit_hotkey)
            self.window.destroy()

        except Exception as e:
            messagebox.showerror("错误", f"保存失败: {e}", parent=self.window)


def show_hotkey_settings(parent, config):
    """显示快捷键设置对话框"""
    dialog = HotkeySettings(parent, config)
    parent.wait_window(dialog.window)
    return dialog.result
