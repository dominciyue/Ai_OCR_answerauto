"""
屏幕截图模块 - 使用临时文件方案
避免Tkinter图片对象在窗口间传递的问题
"""

import tkinter as tk
from PIL import Image, ImageTk
import mss
import logging
import tempfile
import os


logger = logging.getLogger(__name__)


class ScreenCapture:
    """屏幕截图工具"""

    def __init__(self, config=None):
        self.config = config or {}
        self.capture_config = self.config.get('capture', {})

    def capture_fullscreen(self):
        """全屏截图"""
        try:
            with mss.mss() as sct:
                monitor = sct.monitors[1]
                screenshot = sct.grab(monitor)
                img = Image.frombytes('RGB', screenshot.size, screenshot.rgb)
                logger.info(f"全屏截图成功: {img.size}")
                return img
        except Exception as e:
            logger.error(f"全屏截图失败: {e}")
            return None

    def capture_region_interactive(self, callback, parent=None):
        """交互式区域截图

        Args:
            callback: 回调函数
            parent: 父窗口，如果提供则使用Toplevel而不是Tk
        """
        try:
            # 1. 截取全屏
            fullscreen = self.capture_fullscreen()
            if not fullscreen:
                callback(None, None)
                return

            # 2. 保存到临时文件（避免Tkinter图片对象问题）
            temp_file = tempfile.NamedTemporaryFile(suffix='.png', delete=False)
            temp_path = temp_file.name
            temp_file.close()
            fullscreen.save(temp_path)
            logger.info(f"截图已保存到临时文件: {temp_path}")

            # 3. 创建选择器窗口
            selector = RegionSelector(temp_path, fullscreen, self.capture_config, callback, parent)
            selector.start()

            # 4. 清理临时文件
            try:
                os.unlink(temp_path)
            except:
                pass

        except Exception as e:
            logger.error(f"交互式截图失败: {e}")
            callback(None, None)


class RegionSelector:
    """区域选择器"""

    def __init__(self, image_path, original_image, config, callback, parent=None):
        self.image_path = image_path
        self.original_image = original_image
        self.config = config
        self.callback = callback
        self.parent = parent  # 父窗口

        self.start_x = None
        self.start_y = None
        self.rect_id = None

        self.border_color = config.get('border_color', [255, 0, 0])
        self.border_width = config.get('border_width', 2)

    def start(self):
        """启动选区窗口"""
        # 如果有父窗口，使用Toplevel；否则使用Tk
        if self.parent:
            root = tk.Toplevel(self.parent)
        else:
            root = tk.Tk()

        root.title("选择区域")

        # 直接使用原始图片的尺寸（真实屏幕分辨率）
        screen_w = self.original_image.width
        screen_h = self.original_image.height

        logger.info(f"使用真实屏幕尺寸: {screen_w} x {screen_h}")

        # 无边框全屏
        root.overrideredirect(True)
        root.attributes('-topmost', True)
        root.configure(cursor='cross', bg='black')

        # 设置窗口大小和位置
        root.geometry(f"{screen_w}x{screen_h}+0+0")

        # 创建画布 - 使用真实尺寸
        canvas = tk.Canvas(
            root,
            width=screen_w,
            height=screen_h,
            highlightthickness=0,
            bg='black'
        )
        canvas.pack(fill='both', expand=True)

        # 从文件加载图片（使用原始尺寸）
        img = Image.open(self.image_path)
        logger.info(f"图片尺寸: {img.size}")

        photo = ImageTk.PhotoImage(img)
        canvas.create_image(0, 0, anchor=tk.NW, image=photo)

        # 保持引用
        canvas.photo = photo

        # 半透明遮罩
        canvas.create_rectangle(
            0, 0, screen_w, screen_h,
            fill='black', stipple='gray25', outline=''
        )

        # 提示文字
        canvas.create_text(
            screen_w // 2, 50,
            text="拖动鼠标框选题目区域\n按 ESC 取消",
            fill='white',
            font=('Arial', 20, 'bold')
        )

        # 事件处理
        def on_press(event):
            self.start_x = event.x
            self.start_y = event.y
            color = f'#{self.border_color[0]:02x}{self.border_color[1]:02x}{self.border_color[2]:02x}'
            self.rect_id = canvas.create_rectangle(
                self.start_x, self.start_y, self.start_x, self.start_y,
                outline=color, width=self.border_width
            )

        def on_drag(event):
            if self.rect_id:
                canvas.coords(
                    self.rect_id,
                    self.start_x, self.start_y,
                    event.x, event.y
                )

        def on_release(event):
            if self.start_x is None or self.start_y is None:
                return

            x1 = min(self.start_x, event.x)
            y1 = min(self.start_y, event.y)
            x2 = max(self.start_x, event.x)
            y2 = max(self.start_y, event.y)

            if abs(x2 - x1) < 10 or abs(y2 - y1) < 10:
                logger.warning("选区太小")
                root.destroy()
                if self.callback:
                    self.callback(None, None)
                return

            logger.info(f"选区: ({x1}, {y1}, {x2}, {y2})")

            # 使用原始图片对象裁剪
            result_image = self.original_image.crop((x1, y1, x2, y2))

            root.destroy()

            if self.callback:
                self.callback(result_image, (x1, y1, x2, y2))

        def on_cancel(event):
            logger.info("取消截图")
            root.destroy()
            if self.callback:
                self.callback(None, None)

        # 绑定事件
        canvas.bind('<ButtonPress-1>', on_press)
        canvas.bind('<B1-Motion>', on_drag)
        canvas.bind('<ButtonRelease-1>', on_release)
        root.bind('<Escape>', on_cancel)

        root.mainloop()
