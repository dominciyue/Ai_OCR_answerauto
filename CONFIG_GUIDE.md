# AI自动答题系统 - 配置向导

**首次运行配置指南**

## 快速开始

### 方式1：运行配置向导
```bash
python src/main.py
```
首次运行会自动弹出配置向导，按照提示填写即可。

### 方式2：手动配置

1. 复制 `config.example.yaml` 为 `config.yaml`
2. 编辑配置文件：

```yaml
ai:
  provider: "openai"
  api_key: "your-api-key-here"  # 填写你的API密钥
  model: "deepseek-chat"         # 选择模型
  base_url: "https://api.deepseek.com"
```

## 推荐的国产大模型

### 1. DeepSeek（推荐）⭐
- **优势**：性价比最高，新用户送500万tokens
- **价格**：¥1/百万tokens（输入），¥2/百万tokens（输出）
- **申请**：https://platform.deepseek.com/
- **配置**：
```yaml
ai:
  provider: "openai"
  api_key: "sk-xxx"
  model: "deepseek-chat"
  base_url: "https://api.deepseek.com"
```

### 2. 通义千问
- **优势**：阿里云出品，速度快，稳定
- **申请**：https://dashscope.aliyun.com/
- **配置**：
```yaml
ai:
  provider: "openai"
  api_key: "sk-xxx"
  model: "qwen-turbo"
  base_url: "https://dashscope.aliyuncs.com/compatible-mode/v1"
```

### 3. 智谱AI（GLM）
- **优势**：清华出品，效果优秀
- **申请**：https://open.bigmodel.cn/
- **配置**：
```yaml
ai:
  provider: "openai"
  api_key: "xxx"
  model: "glm-4-flash"
  base_url: "https://open.bigmodel.cn/api/paas/v4"
```

### 4. Moonshot（Kimi）
- **优势**：上下文窗口长
- **申请**：https://platform.moonshot.cn/
- **配置**：
```yaml
ai:
  provider: "openai"
  api_key: "sk-xxx"
  model: "moonshot-v1-8k"
  base_url: "https://api.moonshot.cn/v1"
```

### 5. 百川智能
- **优势**：性能稳定
- **申请**：https://platform.baichuan-ai.com/
- **配置**：
```yaml
ai:
  provider: "openai"
  api_key: "sk-xxx"
  model: "Baichuan2-Turbo"
  base_url: "https://api.baichuan-ai.com/v1"
```

### 6. 豆包
- **优势**：字节跳动出品
- **申请**：https://console.volcengine.com/ark
- **配置**：
```yaml
ai:
  provider: "openai"
  api_key: "xxx"
  model: "doubao-pro-4k"
  base_url: "https://ark.cn-beijing.volces.com/api/v3"
```

## 配置说明

所有配置文件位于 `config/config.yaml`：

```yaml
# AI配置
ai:
  provider: "openai"           # 固定为openai（国产模型都兼容OpenAI格式）
  api_key: "your-key"          # 你的API密钥
  model: "deepseek-chat"       # 模型名称
  base_url: "https://..."      # API地址
  timeout: 30                  # 超时时间（秒）
  max_retries: 3               # 最大重试次数

# OCR配置
ocr:
  confidence_threshold: 0.5    # 识别置信度阈值（0.0-1.0）

# 界面配置
gui:
  hotkey: "f9"                 # 快速答题快捷键
  quit_hotkey: "ctrl+q"        # 退出快捷键
  theme: "light"               # 主题：light, dark

# 截图配置
capture:
  border_color: [255, 0, 0]    # 选区边框颜色（RGB）
  border_width: 2              # 边框宽度
```

## 常见问题

### Q: 如何获取API密钥？
A: 访问对应平台官网注册，创建API Key即可。详见 `docs/DeepSeek申请教程.md`

### Q: 哪个模型最便宜？
A: DeepSeek，1000道题约¥1，新用户还送500万tokens免费额度。

### Q: 需要翻墙吗？
A: 不需要！所有推荐的都是国产模型，国内直接访问。

### Q: 配置错误怎么办？
A: 删除 `config/config.yaml`，重新运行程序会弹出配置向导。

---

**详细教程：** [docs/QUICKSTART.md](docs/QUICKSTART.md)
