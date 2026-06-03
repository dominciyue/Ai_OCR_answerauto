"""
测试截图功能
"""
import tkinter as tk
from src.screen_capture import ScreenCapture

def test_callback(image, selection):
    if image:
        print(f"✅ 截图成功: {image.size}")
        print(f"   选区: {selection}")
    else:
        print("❌ 截图已取消")

print("正在测试截图功能...")
print("应该会弹出全屏截图窗口")
print("用鼠标拖动选择区域，按ESC取消\n")

try:
    config = {
        'capture': {
            'border_color': [255, 0, 0],
            'border_width': 2
        }
    }

    capture = ScreenCapture(config)
    capture.capture_region_interactive(test_callback)

except Exception as e:
    print(f"错误: {e}")
    import traceback
    traceback.print_exc()
