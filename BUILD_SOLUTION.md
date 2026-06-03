# 最简单的解决方案

由于你的Anaconda环境中有太多库（pandas、scipy等）导致numpy版本冲突，最简单的方法是：

## 方案1：排除所有不需要的库（推荐）

```powershell
pyinstaller --noconfirm --onefile --windowed --name AI_Answer_System ^
--add-data "config\config.example.yaml;config" ^
--collect-data rapidocr_onnxruntime ^
--exclude-module matplotlib ^
--exclude-module torch ^
--exclude-module pandas ^
--exclude-module scipy ^
--exclude-module IPython ^
--exclude-module sphinx ^
--exclude-module numba ^
--exclude-module dask ^
--exclude-module pyarrow ^
src\main.py
```

## 方案2：使用虚拟环境（更干净）

```powershell
# 创建虚拟环境
python -m venv venv_build

# 激活虚拟环境
.\venv_build\Scripts\activate

# 只安装必要的包
pip install pyinstaller rapidocr-onnxruntime pillow mss keyboard pynput openai anthropic pyyaml

# 打包
pyinstaller --noconfirm --onefile --windowed --name AI_Answer_System --add-data "config\config.example.yaml;config" --collect-data rapidocr_onnxruntime src\main.py

# 退出虚拟环境
deactivate
```

## 方案3：忽略numpy警告继续打包

numpy警告只是警告，可能不会影响实际运行。让打包继续执行，最后测试EXE是否能正常工作。

---

## 推荐使用方案1

直接运行这个命令（已排除不需要的大型库）：

```powershell
pyinstaller --noconfirm --onefile --windowed --name AI_Answer_System --add-data "config\config.example.yaml;config" --collect-data rapidocr_onnxruntime --exclude-module matplotlib --exclude-module torch --exclude-module pandas --exclude-module scipy --exclude-module IPython --exclude-module sphinx --exclude-module numba --exclude-module dask --exclude-module pyarrow --exclude-module pytest --exclude-module distributed src\main.py
```

这样可以大幅减小EXE体积，并避免numpy冲突问题。
