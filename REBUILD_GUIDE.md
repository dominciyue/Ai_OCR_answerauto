# 🎯 重新打包 - 已修复stdout问题

## ✅ 已修复的问题

- ✅ 修复了打包后windowed模式下`sys.stdout.buffer`为None的错误
- ✅ 使用try-except保护，避免崩溃

---

## 📦 现在重新打包

### 方法1：排除不需要的库（推荐）

```powershell
# 清理
Remove-Item -Recurse -Force dist, build -ErrorAction SilentlyContinue
Remove-Item *.spec -ErrorAction SilentlyContinue

# 打包
pyinstaller --noconfirm --onefile --windowed --name AI_Answer_System --add-data "config\config.example.yaml;config" --collect-data rapidocr_onnxruntime --exclude-module matplotlib --exclude-module torch --exclude-module pandas --exclude-module scipy --exclude-module IPython --exclude-module sphinx --exclude-module numba --exclude-module dask --exclude-module pyarrow --exclude-module pytest --exclude-module distributed --exclude-module tables --exclude-module sqlalchemy src\main.py
```

### 方法2：使用虚拟环境（最干净）

```powershell
# 1. 创建虚拟环境
python -m venv venv_build

# 2. 激活
.\venv_build\Scripts\activate

# 3. 安装依赖
pip install -r requirements.txt
pip install pyinstaller

# 4. 打包
pyinstaller --noconfirm --onefile --windowed --name AI_Answer_System --add-data "config\config.example.yaml;config" --collect-data rapidocr_onnxruntime src\main.py

# 5. 退出
deactivate
```

---

## 🧪 测试打包结果

```powershell
cd dist
.\AI_Answer_System.exe
```

应该能正常启动了！

---

## 📝 打包后要做的

1. ✅ 测试EXE功能
2. 创建发布文件夹
3. 复制必要文件（README、LICENSE、CONFIG_GUIDE等）
4. 压缩成ZIP
5. 上传到GitHub Release

---

**选择一个方法重新打包吧！** 🚀
