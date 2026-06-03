"""
GUI界面模块 - 优化版
现代化设计，支持托盘图标和历史记录
"""

import logging
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import threading
from datetime import datetime
from pathlib import Path
import json

logger = logging.getLogger(__name__)


class AnswerSystemGUI:
    """答题系统GUI主类"""

    def __init__(self, config):
        self.config = config
        self.gui_config = config.get('gui', {})

        # 核心模块（延迟加载）
        self.screen_capture = None
        self.ocr_engine = None
        self.ai_client = None

        # 状态
        self.is_processing = False
        self.hotkey_listener = None

        # 主窗口
        self.root = None
        self.status_label = None
        self.log_text = None

        # 历史记录
        self.history = []
        self.history_file = Path("data/history.json")
        self.load_history()

        # 托盘图标
        self.tray_icon = None
        self.enable_tray = self.gui_config.get('enable_tray', True)

    def load_history(self):
        """加载历史记录"""
        try:
            if self.history_file.exists():
                with open(self.history_file, 'r', encoding='utf-8') as f:
                    self.history = json.load(f)
                logger.info(f"加载了 {len(self.history)} 条历史记录")
        except Exception as e:
            logger.error(f"加载历史记录失败: {e}")
            self.history = []

    def save_history(self):
        """保存历史记录"""
        try:
            self.history_file.parent.mkdir(parents=True, exist_ok=True)
            with open(self.history_file, 'w', encoding='utf-8') as f:
                json.dump(self.history[-100:], f, ensure_ascii=False, indent=2)  # 只保留最近100条
        except Exception as e:
            logger.error(f"保存历史记录失败: {e}")

    def add_to_history(self, question, answer):
        """添加到历史记录"""
        self.history.append({
            'time': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'question': question[:200],  # 限制长度
            'answer': answer[:500]
        })
        self.save_history()

    def _init_modules(self):
        """延迟初始化核心模块"""
        if self.screen_capture is None:
            from src.screen_capture import ScreenCapture
            self.screen_capture = ScreenCapture(self.config)
            self.log("✅ 截图模块加载成功")

        if self.ocr_engine is None:
            from src.ocr_engine import OCREngine
            self.log("⏳ 正在加载OCR引擎（首次可能较慢）...")
            self.root.update()
            self.ocr_engine = OCREngine(self.config)
            self.log("✅ OCR引擎加载成功")

        if self.ai_client is None:
            from src.ai_client import AIClient
            self.ai_client = AIClient(self.config)
            self.log("✅ AI客户端加载成功")

    def run(self):
        """启动GUI"""
        self._create_main_window()
        self._setup_hotkeys()
        self._setup_tray_icon()
        self._init_modules()

        self.log("=" * 50)
        self.log("🚀 系统就绪！")
        self.log(f"⌨️  按 {self.gui_config.get('hotkey', 'F9').upper()} 快速截图答题")
        self.log("=" * 50)

        self.root.mainloop()

    def _create_main_window(self):
        """创建主窗口"""
        self.root = tk.Tk()
        self.root.title("AI自动答题系统")
        self.root.geometry("700x600")

        # 设置窗口图标（如果存在）
        try:
            icon_path = Path("icon.ico")
            if icon_path.exists():
                self.root.iconbitmap(str(icon_path))
        except:
            pass

        # 现代化配色
        theme = self.gui_config.get('theme', 'light')
        if theme == 'dark':
            bg_color = '#1e1e1e'
            fg_color = '#ffffff'
            header_bg = '#2d2d30'
            card_bg = '#252526'
            accent_color = '#0e639c'
        else:
            bg_color = '#f5f5f5'
            fg_color = '#333333'
            header_bg = '#4CAF50'
            card_bg = '#ffffff'
            accent_color = '#4CAF50'

        self.root.configure(bg=bg_color)

        # 顶部标题栏
        header_frame = tk.Frame(self.root, bg=header_bg, height=80)
        header_frame.pack(fill='x')
        header_frame.pack_propagate(False)

        title_label = tk.Label(
            header_frame,
            text="🤖 AI自动答题系统",
            font=('Microsoft YaHei UI', 20, 'bold'),
            bg=header_bg,
            fg='white'
        )
        title_label.pack(side='left', padx=20, pady=20)

        version_label = tk.Label(
            header_frame,
            text="v1.0",
            font=('Arial', 10),
            bg=header_bg,
            fg='white'
        )
        version_label.pack(side='right', padx=20)

        # 主容器
        main_container = tk.Frame(self.root, bg=bg_color)
        main_container.pack(fill='both', expand=True, padx=15, pady=15)

        # 状态卡片
        status_card = tk.Frame(main_container, bg=card_bg, relief='flat', bd=0)
        status_card.pack(fill='x', pady=(0, 10))

        status_inner = tk.Frame(status_card, bg=card_bg)
        status_inner.pack(fill='x', padx=15, pady=12)

        tk.Label(
            status_inner,
            text="● 状态",
            font=('Microsoft YaHei UI', 10, 'bold'),
            bg=card_bg,
            fg=fg_color
        ).pack(side='left')

        self.status_label = tk.Label(
            status_inner,
            text="就绪",
            font=('Microsoft YaHei UI', 10),
            bg=card_bg,
            fg=accent_color
        )
        self.status_label.pack(side='left', padx=(10, 0))

        # 按钮区域
        button_card = tk.Frame(main_container, bg=card_bg, relief='flat', bd=0)
        button_card.pack(fill='x', pady=(0, 10))

        button_inner = tk.Frame(button_card, bg=card_bg)
        button_inner.pack(padx=15, pady=15)

        # 主按钮
        start_btn = tk.Button(
            button_inner,
            text=f"🖼️ 截图答题 ({self.gui_config.get('hotkey', 'F9').upper()})",
            font=('Microsoft YaHei UI', 11, 'bold'),
            bg=accent_color,
            fg='white',
            padx=30,
            pady=12,
            command=self.start_capture,
            relief='flat',
            cursor='hand2',
            activebackground='#45a049'
        )
        start_btn.pack(side='left', padx=5)

        # 历史记录按钮
        history_btn = tk.Button(
            button_inner,
            text="📚 历史记录",
            font=('Microsoft YaHei UI', 10),
            bg='#2196F3',
            fg='white',
            padx=20,
            pady=12,
            command=self.show_history,
            relief='flat',
            cursor='hand2',
            activebackground='#1976D2'
        )
        history_btn.pack(side='left', padx=5)

        # 设置按钮
        settings_btn = tk.Button(
            button_inner,
            text="⚙️ 设置",
            font=('Microsoft YaHei UI', 10),
            bg='#FF9800',
            fg='white',
            padx=20,
            pady=12,
            command=self.show_settings,
            relief='flat',
            cursor='hand2',
            activebackground='#F57C00'
        )
        settings_btn.pack(side='left', padx=5)

        # 日志区域
        log_label = tk.Label(
            main_container,
            text="📋 运行日志",
            font=('Microsoft YaHei UI', 10, 'bold'),
            bg=bg_color,
            fg=fg_color,
            anchor='w'
        )
        log_label.pack(fill='x', pady=(5, 5))

        log_card = tk.Frame(main_container, bg=card_bg, relief='flat', bd=0)
        log_card.pack(fill='both', expand=True)

        self.log_text = scrolledtext.ScrolledText(
            log_card,
            font=('Consolas', 9),
            bg=card_bg,
            fg=fg_color,
            wrap=tk.WORD,
            state='disabled',
            relief='flat',
            padx=10,
            pady=10
        )
        self.log_text.pack(fill='both', expand=True)

        # 底部信息栏
        footer_frame = tk.Frame(self.root, bg=bg_color, height=40)
        footer_frame.pack(fill='x', side='bottom')
        footer_frame.pack_propagate(False)

        info_label = tk.Label(
            footer_frame,
            text=f"快捷键: {self.gui_config.get('hotkey', 'F9').upper()} 快速答题 | {self.gui_config.get('quit_hotkey', 'Ctrl+Q').upper()} 退出程序",
            font=('Microsoft YaHei UI', 9),
            bg=bg_color,
            fg='#888888'
        )
        info_label.pack(pady=10)

        # 窗口关闭事件
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def _setup_hotkeys(self):
        """设置快捷键"""
        try:
            import keyboard

            hotkey = self.gui_config.get('hotkey', 'f9')
            quit_hotkey = self.gui_config.get('quit_hotkey', 'ctrl+q')

            keyboard.add_hotkey(hotkey, self.start_capture)
            keyboard.add_hotkey(quit_hotkey, self.quit_app)

            logger.info(f"快捷键已注册: {hotkey}, {quit_hotkey}")

        except Exception as e:
            logger.warning(f"快捷键注册失败: {e}")
            self.log(f"⚠️ 快捷键功能不可用: {e}")

    def _setup_tray_icon(self):
        """设置托盘图标"""
        if not self.enable_tray:
            return

        try:
            from src.tray_icon import TrayIcon
            self.tray_icon = TrayIcon(self)
            self.tray_icon.run()
            logger.info("托盘图标已启用")
            self.log("✅ 托盘图标已启用（可最小化到托盘）")
        except ImportError:
            logger.warning("pystray未安装，托盘功能不可用")
            self.log("⚠️ 托盘功能不可用（需要安装pystray）")
        except Exception as e:
            logger.error(f"托盘图标初始化失败: {e}")
            self.log(f"⚠️ 托盘图标初始化失败: {e}")

    def log(self, message):
        """添加日志"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_message = f"[{timestamp}] {message}\n"

        if self.log_text:
            self.log_text.configure(state='normal')
            self.log_text.insert('end', log_message)
            self.log_text.see('end')
            self.log_text.configure(state='disabled')

        logger.info(message)

    def update_status(self, status, color='#4CAF50'):
        """更新状态"""
        if self.status_label:
            self.status_label.config(text=status, fg=color)

    def start_capture(self):
        """开始截图识别"""
        if self.is_processing:
            self.log("⚠️ 正在处理中，请稍候...")
            return

        self.log("\n" + "=" * 50)
        self.log("🖼️ 启动截图...")
        self.update_status("截图中...", '#FF9800')

        # 完全隐藏主窗口
        self.root.withdraw()

        # 使用after延迟执行，让窗口有时间隐藏
        self.root.after(200, self._do_capture)

    def _do_capture(self):
        """执行截图（在主线程中）"""
        self.is_processing = True

        # 截图回调
        def on_capture_done(image, selection):
            if image is None:
                self.log("❌ 截图已取消")
                self.root.deiconify()
                self.update_status("就绪", '#4CAF50')
                self.is_processing = False
                return

            self.log(f"✅ 截图成功: {image.size}")

            # 恢复主窗口
            self.root.deiconify()

            # 在后台线程中处理OCR和AI
            def process_in_background():
                try:
                    # OCR识别
                    self.update_status("识别中...", '#2196F3')
                    self.log("🔍 正在进行OCR识别...")

                    question_text = self.ocr_engine.recognize(image)

                    if not question_text:
                        self.log("❌ 未识别到文字内容")
                        self.root.after(0, lambda: messagebox.showwarning("提示", "未识别到文字，请重试"))
                        self.update_status("就绪", '#4CAF50')
                        self.is_processing = False
                        return

                    self.log(f"✅ OCR识别成功:")
                    self.log(f"   {question_text[:100]}...")

                    # AI问答
                    self.update_status("AI分析中...", '#9C27B0')
                    self.log("🤖 正在请求AI分析...")

                    answer = self.ai_client.answer_question(question_text)

                    if answer:
                        self.log("✅ AI回答完成")
                        self.update_status("完成", '#4CAF50')

                        # 添加到历史记录
                        self.add_to_history(question_text, answer)

                        # 在主线程中显示结果窗口
                        self.root.after(0, lambda: self.show_result_window(question_text, answer))
                    else:
                        self.log("❌ AI回答失败")
                        self.root.after(0, lambda: messagebox.showerror("错误", "AI回答失败，请检查配置或网络"))
                        self.update_status("就绪", '#4CAF50')

                except Exception as e:
                    logger.error(f"处理失败: {e}", exc_info=True)
                    self.log(f"❌ 处理失败: {e}")
                    self.root.after(0, lambda: messagebox.showerror("错误", f"处理失败: {e}"))
                    self.update_status("就绪", '#4CAF50')

                finally:
                    self.is_processing = False

            threading.Thread(target=process_in_background, daemon=True).start()

        try:
            # 执行交互式截图（在主线程中）- 传入父窗口
            self.screen_capture.capture_region_interactive(on_capture_done, parent=self.root)
        except Exception as e:
            logger.error(f"截图失败: {e}", exc_info=True)
            self.log(f"❌ 截图失败: {e}")
            self.root.deiconify()
            self.update_status("就绪", '#4CAF50')
            self.is_processing = False

    def _capture_and_process(self):
        """截图并处理（已废弃，保留以兼容）"""
        pass

    def show_result_window(self, question, answer):
        """显示结果窗口"""
        result_win = tk.Toplevel(self.root)
        result_win.title("📝 AI答案")
        result_win.geometry("750x650")

        # 置顶
        result_win.attributes('-topmost', True)

        # 透明度
        opacity = self.gui_config.get('window_opacity', 0.95)
        result_win.attributes('-alpha', opacity)

        # 主题色
        theme = self.gui_config.get('theme', 'light')
        if theme == 'dark':
            bg_color = '#1e1e1e'
            card_bg = '#252526'
            fg_color = '#ffffff'
        else:
            bg_color = '#f5f5f5'
            card_bg = '#ffffff'
            fg_color = '#333333'

        result_win.configure(bg=bg_color)

        # 题目区域
        question_label = tk.Label(
            result_win,
            text="📋 识别的题目",
            font=('Microsoft YaHei UI', 12, 'bold'),
            bg=bg_color,
            fg=fg_color,
            anchor='w'
        )
        question_label.pack(fill='x', padx=15, pady=(15, 5))

        question_frame = tk.Frame(result_win, bg=card_bg)
        question_frame.pack(fill='both', expand=False, padx=15, pady=5)

        question_text = scrolledtext.ScrolledText(
            question_frame,
            font=('Microsoft YaHei UI', 10),
            wrap=tk.WORD,
            height=8,
            bg=card_bg,
            fg=fg_color,
            relief='flat',
            padx=10,
            pady=10
        )
        question_text.pack(fill='both', expand=True)
        question_text.insert('1.0', question)
        question_text.configure(state='disabled')

        # 答案区域
        answer_label = tk.Label(
            result_win,
            text="✅ AI答案",
            font=('Microsoft YaHei UI', 12, 'bold'),
            bg=bg_color,
            fg='#4CAF50',
            anchor='w'
        )
        answer_label.pack(fill='x', padx=15, pady=(15, 5))

        answer_frame = tk.Frame(result_win, bg=card_bg)
        answer_frame.pack(fill='both', expand=True, padx=15, pady=5)

        answer_text = scrolledtext.ScrolledText(
            answer_frame,
            font=('Microsoft YaHei UI', 11),
            wrap=tk.WORD,
            bg=card_bg,
            fg=fg_color,
            relief='flat',
            padx=10,
            pady=10
        )
        answer_text.pack(fill='both', expand=True)
        answer_text.insert('1.0', answer)
        answer_text.configure(state='disabled')

        # 按钮
        button_frame = tk.Frame(result_win, bg=bg_color)
        button_frame.pack(fill='x', padx=15, pady=15)

        copy_btn = tk.Button(
            button_frame,
            text="📋 复制答案",
            font=('Microsoft YaHei UI', 10),
            bg='#2196F3',
            fg='white',
            padx=20,
            pady=10,
            command=lambda: self._copy_to_clipboard(answer, result_win),
            relief='flat',
            cursor='hand2'
        )
        copy_btn.pack(side='left', padx=(0, 10))

        close_btn = tk.Button(
            button_frame,
            text="关闭",
            font=('Microsoft YaHei UI', 10),
            bg='#757575',
            fg='white',
            padx=20,
            pady=10,
            command=result_win.destroy,
            relief='flat',
            cursor='hand2'
        )
        close_btn.pack(side='left')

        # 自动关闭
        auto_close = self.gui_config.get('auto_close_seconds', 0)
        if auto_close > 0:
            result_win.after(auto_close * 1000, result_win.destroy)

    def show_history(self):
        """显示历史记录"""
        history_win = tk.Toplevel(self.root)
        history_win.title("📚 历史记录")
        history_win.geometry("800x600")

        # 主题色
        theme = self.gui_config.get('theme', 'light')
        bg_color = '#f5f5f5' if theme == 'light' else '#1e1e1e'
        fg_color = '#333333' if theme == 'light' else '#ffffff'

        history_win.configure(bg=bg_color)

        # 标题
        title_label = tk.Label(
            history_win,
            text="📚 答题历史记录",
            font=('Microsoft YaHei UI', 16, 'bold'),
            bg=bg_color,
            fg=fg_color
        )
        title_label.pack(pady=15)

        # 列表框
        list_frame = tk.Frame(history_win, bg=bg_color)
        list_frame.pack(fill='both', expand=True, padx=15, pady=(0, 15))

        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.pack(side='right', fill='y')

        history_list = tk.Listbox(
            list_frame,
            font=('Microsoft YaHei UI', 10),
            bg='white' if theme == 'light' else '#252526',
            fg=fg_color,
            yscrollcommand=scrollbar.set,
            relief='flat'
        )
        history_list.pack(side='left', fill='both', expand=True)
        scrollbar.config(command=history_list.yview)

        # 加载历史记录
        if not self.history:
            history_list.insert('end', "暂无历史记录")
        else:
            for i, item in enumerate(reversed(self.history)):
                display_text = f"[{item['time']}] {item['question'][:50]}..."
                history_list.insert('end', display_text)

        # 查看详情
        def view_detail(event):
            selection = history_list.curselection()
            if selection and self.history:
                index = len(self.history) - 1 - selection[0]
                item = self.history[index]
                self.show_result_window(item['question'], item['answer'])

        history_list.bind('<Double-Button-1>', view_detail)

        # 按钮
        button_frame = tk.Frame(history_win, bg=bg_color)
        button_frame.pack(pady=10)

        clear_btn = tk.Button(
            button_frame,
            text="清空历史",
            font=('Microsoft YaHei UI', 10),
            bg='#f44336',
            fg='white',
            padx=20,
            pady=10,
            command=lambda: self.clear_history(history_win),
            relief='flat',
            cursor='hand2'
        )
        clear_btn.pack(side='left', padx=5)

        close_btn = tk.Button(
            button_frame,
            text="关闭",
            font=('Microsoft YaHei UI', 10),
            bg='#757575',
            fg='white',
            padx=20,
            pady=10,
            command=history_win.destroy,
            relief='flat',
            cursor='hand2'
        )
        close_btn.pack(side='left', padx=5)

    def clear_history(self, window):
        """清空历史记录"""
        if messagebox.askyesno("确认", "确定要清空所有历史记录吗？", parent=window):
            self.history = []
            self.save_history()
            messagebox.showinfo("成功", "历史记录已清空", parent=window)
            window.destroy()

    def show_settings(self):
        """显示设置窗口"""
        from src.hotkey_settings import show_hotkey_settings

        result = show_hotkey_settings(self.root, self.config)
        if result:
            self.log(f"✅ 快捷键已更新，请重启程序生效")

    def _copy_to_clipboard(self, text, window):
        """复制到剪贴板"""
        window.clipboard_clear()
        window.clipboard_append(text)
        messagebox.showinfo("成功", "答案已复制到剪贴板！", parent=window)

    def on_closing(self):
        """窗口关闭事件"""
        if self.enable_tray and self.tray_icon:
            # 有托盘图标时，询问是否最小化到托盘
            result = messagebox.askyesnocancel(
                "提示",
                "要最小化到系统托盘吗？\n\n是(Y) - 最小化到托盘\n否(N) - 退出程序\n取消 - 继续使用"
            )
            if result is True:  # 是 - 最小化到托盘
                self.root.withdraw()
                return
            elif result is False:  # 否 - 退出
                self.quit_app()
            # 取消 - 什么都不做
        else:
            # 没有托盘图标，直接询问是否退出
            if messagebox.askokcancel("退出", "确定要退出吗？"):
                self.quit_app()

    def quit_app(self):
        """退出程序"""
        logger.info("用户退出程序")

        # 停止托盘图标
        if self.tray_icon:
            try:
                self.tray_icon.stop()
            except:
                pass

        # 卸载快捷键
        try:
            import keyboard
            keyboard.unhook_all()
        except:
            pass

        self.root.quit()
        self.root.destroy()
