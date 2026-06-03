"""
简单的截图窗口测试 - 不使用遮罩
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
root.configure(bg='red')  # 红色背景，方便看出问题

# 创建画布
canvas = tk.Canvas(root, width=screen_w, height=screen_h, highlightthickness=0)
canvas.pack()

# 显示图片
photo = ImageTk.PhotoImage(img)
canvas.create_image(0, 0, anchor=tk.NW, image=photo)

# 添加文字标识
canvas.create_text(
    screen_w // 2, screen_h // 2,
    text=f"截图: {img.size}\n屏幕: {screen_w}x{screen_h}",
    fill='red',
    font=('Arial', 30, 'bold')
)

print("\n窗口已显示，按任意键关闭...")

root.bind('<Key>', lambda e: root.destroy())
root.bind('<Button-1>', lambda e: root.destroy())

root.mainloop()

print("测试完成")
