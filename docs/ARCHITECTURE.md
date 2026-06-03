# 项目文件结构

```
ai自动答题系统/
│
├── src/                          # 源代码目录
│   ├── __init__.py              # 包初始化
│   ├── main.py                  # 主程序入口
│   ├── gui.py                   # GUI界面模块
│   ├── screen_capture.py        # 屏幕截图模块
│   ├── ocr_engine.py            # OCR识别引擎
│   └── ai_client.py             # AI客户端（支持多种API）
│
├── config/                       # 配置文件目录
│   ├── config.yaml              # 实际配置（包含密钥，不提交到Git）
│   └── config.example.yaml      # 配置示例文件
│
├── docs/                         # 文档目录
│   └── QUICKSTART.md            # 快速开始指南
│
├── tests/                        # 测试目录
│   └── test_modules.py          # 模块测试脚本
│
├── logs/                         # 日志目录（自动创建）
│   └── app.log                  # 应用日志
│
├── screenshots/                  # 截图保存目录（可选，自动创建）
│   └── *.png                    # 保存的截图文件
│
├── requirements.txt             # Python依赖列表
├── README.md                    # 项目说明文档
├── LICENSE                      # 开源协议和免责声明
├── .gitignore                   # Git忽略文件配置
│
├── install.bat                  # Windows安装脚本
├── install.sh                   # Linux/Mac安装脚本
├── run.bat                      # Windows启动脚本
└── run.sh                       # Linux/Mac启动脚本
```

## 核心模块说明

### 1. main.py - 主程序
- 加载配置文件
- 初始化日志系统
- 启动GUI界面
- 程序入口

### 2. gui.py - GUI界面
- 主窗口界面
- 日志显示区域
- 结果展示窗口
- 快捷键监听
- 状态管理

### 3. screen_capture.py - 屏幕截图
- 全屏截图功能
- 交互式区域选择
- 选区可视化反馈
- 支持ESC取消

### 4. ocr_engine.py - OCR识别
- 基于PaddleOCR
- 支持中英文识别
- 置信度过滤
- 详细信息返回

### 5. ai_client.py - AI客户端
- 统一的AI接口
- 支持OpenAI GPT
- 支持Anthropic Claude
- 支持阿里通义千问
- 自动重试机制
- 错误处理

## 配置文件结构

### config.yaml
```yaml
ai:              # AI配置
  provider       # 提供商（openai/claude/qwen）
  api_key        # API密钥
  model          # 模型名称
  base_url       # API基础URL（可选）
  timeout        # 超时时间
  max_retries    # 最大重试次数

ocr:             # OCR配置
  lang           # 语言设置
  use_gpu        # GPU加速
  confidence_threshold  # 置信度阈值

gui:             # 界面配置
  hotkey         # 启动快捷键
  quit_hotkey    # 退出快捷键
  window_opacity # 窗口透明度
  auto_close_seconds  # 自动关闭时间
  theme          # 主题（light/dark）

capture:         # 截图配置
  save_screenshot      # 是否保存
  screenshot_dir       # 保存目录
  border_color         # 边框颜色
  border_width         # 边框宽度

logging:         # 日志配置
  level          # 日志级别
  save_to_file   # 保存到文件
  log_file       # 日志文件路径
```

## 数据流程

```
用户按F9
    ↓
启动截图模块
    ↓
显示全屏截图
    ↓
用户拖动选择区域
    ↓
获取选区图片
    ↓
OCR识别文字
    ↓
发送给AI分析
    ↓
显示答案窗口
```

## 扩展点

1. **新增AI提供商**：在 `ai_client.py` 中添加新的初始化和调用方法
2. **自定义提示词**：修改 `ai_client.py` 中的 `_build_prompt()` 方法
3. **新增快捷键**：在 `gui.py` 中的 `_setup_hotkeys()` 方法添加
4. **保存答案历史**：可以在 `gui.py` 中添加数据库或文件保存逻辑
5. **浏览器插件版本**：使用相同的OCR和AI逻辑，配合浏览器扩展API
