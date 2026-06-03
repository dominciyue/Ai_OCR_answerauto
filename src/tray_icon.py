"""
系统托盘图标模块
"""
import logging
from PIL import Image, ImageDraw
import pystray
from pystray import MenuItem as item
import threading

logger = logging.getLogger(__name__)


class TrayIcon:
    """系统托盘图标"""

    def __init__(self, gui_instance):
        self.gui = gui_instance
        self.icon = None
        self.running = False

    def create_image(self):
        """创建托盘图标"""
        # 创建一个简单的图标（绿色圆圈，中间有"AI"字样）
        width = 64
        height = 64
        image = Image.new('RGB', (width, height), color='white')
        dc = ImageDraw.Draw(image)

        # 绘制绿色圆圈
        dc.ellipse([4, 4, width-4, height-4], fill='#4CAF50', outline='#2E7D32', width=2)

        # 绘制"AI"文字（简化版，使用矩形模拟）
        # 这里简化处理，实际应该使用字体
        dc.rectangle([20, 22, 24, 42], fill='white')  # A的左边
        dc.rectangle([28, 22, 32, 42], fill='white')  # A的右边
        dc.rectangle([20, 22, 32, 26], fill='white')  # A的横线
        dc.rectangle([40, 22, 44, 42], fill='white')  # I

        return image

    def setup(self):
        """设置托盘图标"""
        try:
            # 创建菜单
            menu = pystray.Menu(
                item('显示主窗口', self.show_window, default=True),
                item('快速答题 (F9)', self.quick_answer),
                item('历史记录', self.show_history),
                pystray.Menu.SEPARATOR,
                item('退出', self.quit_app)
            )

            # 创建图标
            self.icon = pystray.Icon(
                "AI答题系统",
                self.create_image(),
                "AI自动答题系统",
                menu
            )

            logger.info("托盘图标初始化成功")
            return True

        except Exception as e:
            logger.error(f"托盘图标初始化失败: {e}")
            return False

    def run(self):
        """运行托盘图标（在独立线程中）"""
        if not self.icon:
            self.setup()

        self.running = True

        def run_icon():
            try:
                self.icon.run()
            except Exception as e:
                logger.error(f"托盘图标运行错误: {e}")

        thread = threading.Thread(target=run_icon, daemon=True)
        thread.start()

    def stop(self):
        """停止托盘图标"""
        if self.icon:
            try:
                self.icon.stop()
                self.running = False
                logger.info("托盘图标已停止")
            except Exception as e:
                logger.error(f"停止托盘图标失败: {e}")

    def show_window(self, icon=None, item=None):
        """显示主窗口"""
        if self.gui.root:
            self.gui.root.deiconify()
            self.gui.root.lift()
            self.gui.root.focus_force()

    def hide_window(self):
        """隐藏主窗口到托盘"""
        if self.gui.root:
            self.gui.root.withdraw()

    def quick_answer(self, icon=None, item=None):
        """快速答题"""
        self.gui.start_capture()

    def show_history(self, icon=None, item=None):
        """显示历史记录"""
        self.show_window()
        self.gui.show_history()

    def quit_app(self, icon=None, item=None):
        """退出程序"""
        self.stop()
        self.gui.quit_app()
