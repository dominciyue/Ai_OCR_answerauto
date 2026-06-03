# AI自动答题系统

<div align="center">

![Version](https://img.shields.io/badge/version-1.0.0-blue)
![Python](https://img.shields.io/badge/python-3.8+-green)
![License](https://img.shields.io/badge/license-MIT-orange)
![Stars](https://img.shields.io/github/stars/dominciyue/Ai_OCR_answerauto?style=social)

**🤖 一键截图识别题目，AI智能生成答案**

**支持多种国产大模型 | 离线OCR | 完全免费开源**

[快速开始](#快速开始) • [功能特性](#功能特性) • [支持的AI模型](#支持的ai模型) • [下载](https://github.com/dominciyue/Ai_OCR_answerauto/releases)

</div>

---

## 📖 简介

AI自动答题系统是一款**完全开源免费**的智能答题助手，特别针对国内用户优化：

- 🇨🇳 **支持6种国产大模型** - DeepSeek、通义千问、智谱AI、Moonshot、百川、豆包
- 🔍 **离线OCR识别** - RapidOCR本地处理，无需联网，完全免费
- 💰 **超低成本** - DeepSeek：1000道题仅需¥1
- 🚫 **无需翻墙** - 所有推荐模型均为国产，国内直接访问
- 📚 **开箱即用** - 3分钟配置完成，简单易用

---

## ✨ 功能特性

### 核心功能
- ✅ **一键截图** - F9快速截取题目，可自定义快捷键
- ✅ **智能OCR** - RapidOCR离线引擎，中英文混合识别准确率高
- ✅ **多模型支持** - 6种国产大模型随意切换
- ✅ **历史记录** - 自动保存最近100条答题记录
- ✅ **现代化界面** - 简洁美观的GUI设计

### 技术优势
- 🚀 **完全离线OCR** - 无需API密钥，无额度限制
- 💰 **超低成本** - DeepSeek最便宜，新用户送500万tokens
- 🔒 **隐私安全** - OCR本地处理，题目不上传
- 📦 **开箱即用** - 配置向导引导，无需复杂设置
- 🎨 **高度可定制** - 支持自定义快捷键、AI模型、界面主题

---

## 🤖 支持的AI模型

### 推荐使用（国产大模型）

| 模型 | 优势 | 价格 | 申请地址 |
|-----|------|------|---------|
| **DeepSeek** ⭐ | 性价比最高，新用户送500万tokens | ¥1/百万tokens | [申请](https://platform.deepseek.com/) |
| **通义千问** | 阿里云出品，速度快，稳定 | 按量付费 | [申请](https://dashscope.aliyun.com/) |
| **智谱AI** | 清华出品，效果优秀 | 按量付费 | [申请](https://open.bigmodel.cn/) |
| **Moonshot** | Kimi出品，上下文窗口长 | 按量付费 | [申请](https://platform.moonshot.cn/) |
| **百川智能** | 性能稳定 | 按量付费 | [申请](https://platform.baichuan-ai.com/) |
| **豆包** | 字节跳动出品 | 按量付费 | [申请](https://console.volcengine.com/ark) |

**全部支持国内访问，无需翻墙！**

详细配置教程：[CONFIG_GUIDE.md](CONFIG_GUIDE.md)

---

## 🚀 快速开始

### 方法一：下载EXE（推荐）

1. 从 [Releases](https://github.com/dominciyue/Ai_OCR_answerauto/releases) 下载最新版本
2. 解压到任意目录
3. 双击运行 `AI答题系统.exe`
4. 首次启动选择AI模型（推荐DeepSeek）
5. 填入API密钥
6. 按F9开始使用！

### 方法二：从源码运行

```bash
# 1. 克隆仓库
git clone https://github.com/dominciyue/Ai_OCR_answerauto.git
cd Ai_OCR_answerauto

# 2. 安装依赖
pip install -r requirements.txt

# 3. 运行程序
python src/main.py
```

---

## 🔑 获取API密钥

### DeepSeek（强烈推荐）⭐

**为什么选择DeepSeek？**
- 💰 **超便宜**：1000道题≈¥1
- 🎁 **免费额度**：新用户送500万tokens（约5000-10000道题）
- 🇨🇳 **国内友好**：支持手机号注册，支付宝/微信充值
- ⚡ **效果优秀**：媲美GPT-4的回答质量

**申请步骤（3分钟）：**
1. 访问 [DeepSeek平台](https://platform.deepseek.com/)
2. 注册账号（手机号/邮箱）
3. 创建API Key
4. 复制密钥到程序

📖 **详细教程**：[DeepSeek申请教程](docs/DeepSeek申请教程.md)

### 其他模型

所有支持的国产模型申请教程：[CONFIG_GUIDE.md](CONFIG_GUIDE.md)

---

## 📸 使用方法

### 基本使用

1. **启动程序** - 运行 `AI答题系统.exe` 或 `python src/main.py`
2. **按F9截图** - 用鼠标框选题目区域
3. **查看答案** - AI自动识别并生成答案
4. **查看历史** - 点击"历史记录"按钮回顾之前的答题

### 快捷键

| 快捷键 | 功能 |
|-------|------|
| `F9` | 快速截图答题（可自定义） |
| `Ctrl+Q` | 退出程序 |
| `ESC` | 取消截图 |

---

## 💡 使用技巧

### 截图技巧
- ✅ 框选完整题目（题干+选项）
- ✅ 确保文字清晰（打印体最佳）
- ✅ 避免多余内容（如水印、边框）
- ❌ 避免手写字（识别率较低）

### 费用说明（以DeepSeek为例）

- **免费额度**：500万tokens ≈ 5000-10000道题
- **付费价格**：
  - 1道题 ≈ ¥0.001（一厘钱）
  - 100道题 ≈ ¥0.10（一毛钱）
  - 1000道题 ≈ ¥1（一块钱）

**极其便宜，放心使用！**

---

## 🛠️ 配置说明

### 切换AI模型

编辑 `config/config.yaml`，参考 [config.example.yaml](config/config.example.yaml)：

```yaml
# DeepSeek
ai:
  provider: "openai"
  api_key: "sk-xxx"
  model: "deepseek-chat"
  base_url: "https://api.deepseek.com"

# 通义千问
ai:
  provider: "openai"
  api_key: "sk-xxx"
  model: "qwen-turbo"
  base_url: "https://dashscope.aliyuncs.com/compatible-mode/v1"
```

**所有支持的模型配置**：[CONFIG_GUIDE.md](CONFIG_GUIDE.md)

### 自定义快捷键

点击主界面"⚙️ 设置"按钮，可修改快捷键。

---

## 📚 文档

- [快速开始指南](docs/QUICKSTART.md)
- [配置指南 - 国产大模型](CONFIG_GUIDE.md)
- [DeepSeek申请教程](docs/DeepSeek申请教程.md)
- [常见问题FAQ](#常见问题)

---

## ❓ 常见问题

### Q: 需要翻墙吗？
**A:** 不需要！所有推荐的都是国产模型，国内直接访问。

### Q: 哪个模型最便宜？
**A:** DeepSeek，1000道题约¥1，新用户还送500万tokens免费额度。

### Q: OCR识别不准确怎么办？
**A:** 
- 确保文字清晰（打印体最佳）
- 尽量截取完整题目
- 避免复杂背景

### Q: 快捷键冲突怎么办？
**A:** 点击"设置"按钮，修改为其他快捷键（如F10、F11）。

### Q: 支持哪些AI模型？
**A:** 
- ✅ 国产：DeepSeek、通义千问、智谱AI、Moonshot、百川、豆包
- ✅ 国际：OpenAI GPT、Claude（需要翻墙）

---

## 🎯 使用场景

- ✏️ **学习辅助** - 理解题目解题思路
- 📝 **作业帮助** - 快速获取答案和解析
- 🎓 **知识巩固** - 查看详细解题步骤
- 💡 **思路启发** - AI分析题目类型和考点

⚠️ **免责声明**：本工具仅供学习研究使用，请遵守学术诚信政策。

---

## 🔧 技术栈

- **OCR**: RapidOCR（离线，开源）
- **AI**: DeepSeek / 通义千问 / 智谱AI / Moonshot / 百川 / 豆包
- **GUI**: Tkinter
- **截图**: mss
- **快捷键**: keyboard

---

## 🤝 贡献

欢迎贡献代码、报告问题、提出建议！

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 提交 Pull Request

---

## 📄 开源协议

本项目采用 [MIT](LICENSE) 协议开源。

---

## 🙏 致谢

- [RapidOCR](https://github.com/RapidAI/RapidOCR) - 优秀的离线OCR引擎
- [DeepSeek](https://www.deepseek.com/) - 高性价比的AI服务
- 所有贡献者和使用者

---

## 📞 联系方式

- 📧 问题反馈：[提交Issue](https://github.com/dominciyue/Ai_OCR_answerauto/issues)
- 💬 讨论交流：[GitHub Discussions](https://github.com/dominciyue/Ai_OCR_answerauto/discussions)

---

<div align="center">

**如果觉得项目有帮助，请点个⭐Star支持一下！**

Made with ❤️ by [dominciyue](https://github.com/dominciyue)

</div>
