"""
测试截图功能 - 调试版
"""
import tkinter as tk
from PIL import Image
import mss

print("=" * 60)
print("测试截图功能")
print("=" * 60)

# 1. 测试mss截图
print("\n[1] 测试mss全屏截图...")
try:
    with mss.mss() as sct:
        monitor = sct.monitors[1]
        print(f"主显示器信息: {monitor}")

        screenshot = sct.grab(monitor)
        print(f"截图尺寸: {screenshot.size}")

        # 转换为PIL Image
        img = Image.frombytes('RGB', screenshot.size, screenshot.rgb)
        print(f"PIL Image尺寸: {img.size}")
        print(f"PIL Image模式: {img.mode}")

        # 保存到文件检查
        img.save("test_screenshot.png")
        print("✅ 截图已保存到 test_screenshot.png，请检查是否正常")

except Exception as e:
    print(f"❌ 截图失败: {e}")
    import traceback
    traceback.print_exc()

# 2. 测试Tkinter屏幕尺寸
print("\n[2] 测试Tkinter屏幕尺寸...")
try:
    root = tk.Tk()
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    print(f"Tkinter屏幕尺寸: {screen_width} x {screen_height}")
    root.destroy()
except Exception as e:
    print(f"❌ 获取屏幕尺寸失败: {e}")

print("\n" + "=" * 60)
print("测试完成")
print("=" * 60)
print("\n请检查:")
print("1. test_screenshot.png 是否正常显示屏幕内容")
print("2. 截图尺寸是否与Tkinter屏幕尺寸一致")
