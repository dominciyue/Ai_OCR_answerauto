"""
截图显示测试 - 加强版
"""
import tkinter as tk
from PIL import Image, ImageTk
import mss

print("正在测试截图显示...")

# 截图
with mss.mss() as sct:
    monitor = sct.monitors[1]
    screenshot = sct.grab(monitor)
    img = Image.frombytes('RGB', screenshot.size, screenshot.rgb)
    print(f"截图尺寸: {img.size}")

# 创建窗口
root = tk.Tk()

# 获取屏幕尺寸
screen_w = root.winfo_screenwidth()
screen_h = root.winfo_screenheight()
print(f"屏幕尺寸: {screen_w} x {screen_h}")

# 设置窗口
root.overrideredirect(True)
root.geometry(f"{screen_w}x{screen_h}+0+0")
root.attributes('-topmost', True)

# 创建画布
canvas = tk.Canvas(root, width=screen_w, height=screen_h, highlightthickness=0, bg='blue')
canvas.pack(fill='both', expand=True)

# 显示图片
photo = ImageTk.PhotoImage(img)
img_id = canvas.create_image(0, 0, anchor=tk.NW, image=photo)

# 添加半透明遮罩测试
overlay_id = canvas.create_rectangle(
    0, 0, screen_w, screen_h,
    fill='black', stipple='gray25', outline=''
)

# 添加文字
text_id = canvas.create_text(
    screen_w // 2, 100,
    text="这是半透明遮罩效果\n应该能看到下面的截图内容\n点击任意位置关闭",
    fill='yellow',
    font=('Arial', 24, 'bold'),
    justify=tk.CENTER
)

print("\n窗口已显示")
print("- 应该能看到屏幕截图")
print("- 上面有半透明黑色遮罩")
print("- 最上面有黄色文字")
print("\n点击任意位置关闭...")

root.bind('<Button-1>', lambda e: root.destroy())
root.bind('<Escape>', lambda e: root.destroy())

root.mainloop()

print("测试完成")
