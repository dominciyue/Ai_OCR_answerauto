# 快速开始指南

## 1. 安装依赖

```bash
pip install -r requirements.txt
```

**注意事项：**
- 首次安装PaddleOCR会下载模型文件（约几百MB），需要等待
- 如果安装paddlepaddle失败，可以访问 https://www.paddlepaddle.org.cn/ 选择合适的版本
- Windows用户可能需要安装Microsoft Visual C++ 14.0或更高版本

## 2. 配置API密钥

打开 `config/config.yaml`，修改以下配置：

```yaml
ai:
  provider: "openai"  # 或 claude, qwen
  api_key: "sk-xxxxxxxxxxxx"  # 填入你的API密钥
  model: "gpt-4o"  # 选择模型
```

### 获取API密钥

**OpenAI:**
1. 访问 https://platform.openai.com/
2. 注册账号并创建API密钥
3. 推荐模型：`gpt-4o`（快速且便宜）或 `gpt-4`（更强大）

**Claude (Anthropic):**
1. 访问 https://console.anthropic.com/
2. 注册账号并创建API密钥
3. 推荐模型：`claude-3-5-sonnet-20241022`

**通义千问 (阿里云):**
1. 访问 https://dashscope.aliyun.com/
2. 开通服务并获取API Key
3. 推荐模型：`qwen-plus` 或 `qwen-turbo`
4. 配置示例：
```yaml
ai:
  provider: "qwen"
  api_key: "sk-xxxxx"
  model: "qwen-plus"
  base_url: "https://dashscope.aliyuncs.com/compatible-mode/v1"
```

## 3. 运行程序

```bash
python src/main.py
```

## 4. 使用方法

1. 程序启动后会显示主界面
2. 按 **F9** 键（或点击"开始识别"按钮）
3. 屏幕会显示当前画面，用鼠标拖动框选题目区域
4. 松开鼠标后自动识别并获取答案
5. 答案会在新窗口中展示

## 5. 常见问题

### Q: 提示"未识别到文字"？
- 确保截图区域包含清晰的文字
- 尝试放大题目后再截图
- 检查OCR配置中的语言设置是否正确

### Q: AI回答失败？
- 检查API密钥是否正确
- 确保网络可以访问API服务
- 查看日志了解具体错误信息

### Q: OCR识别不准确？
- 使用更清晰的截图
- 调整 `config.yaml` 中的 `confidence_threshold` 参数
- 对于复杂排版，可以尝试分段截图

### Q: 快捷键不生效？
- Windows系统可能需要管理员权限
- 检查是否有其他程序占用了相同快捷键
- 可以在配置文件中修改快捷键

### Q: 程序启动很慢？
- 首次启动需要加载OCR模型（约10-30秒）
- 后续启动会快很多
- 可以考虑启用GPU加速（需要CUDA环境）

## 6. 高级配置

### 启用GPU加速（可选）

如果你有NVIDIA显卡和CUDA环境：

```yaml
ocr:
  use_gpu: true
```

需要安装GPU版本的PaddlePaddle：
```bash
pip install paddlepaddle-gpu
```

### 自定义快捷键

```yaml
gui:
  hotkey: "f10"  # 改为F10
  quit_hotkey: "alt+q"  # 改为Alt+Q
```

### 保存截图（用于调试）

```yaml
capture:
  save_screenshot: true
  screenshot_dir: "./screenshots"
```

### 调整答案窗口

```yaml
gui:
  window_opacity: 0.9  # 透明度
  auto_close_seconds: 30  # 30秒后自动关闭（0为不关闭）
  theme: "dark"  # 深色主题
```

## 7. 日志查看

日志文件位于 `logs/app.log`，包含详细的运行信息，有助于排查问题。

## 8. 更新

拉取最新代码后，更新依赖：
```bash
pip install -r requirements.txt --upgrade
```
