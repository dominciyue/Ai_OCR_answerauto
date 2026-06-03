# AI自动答题系统

<div align="center">

![Version](https://img.shields.io/badge/version-1.0.0-blue)
![Python](https://img.shields.io/badge/python-3.8+-green)
![License](https://img.shields.io/badge/license-MIT-orange)
![Stars](https://img.shields.io/github/stars/dominciyue/Ai_OCR_answerauto?style=social)

**🤖 一键截图识别题目，AI智能生成答案**

[快速开始](#快速开始) • [功能特性](#功能特性) • [下载](#下载) • [文档](docs/QUICKSTART.md) • [常见问题](#常见问题)

</div>

---

## 📖 简介

AI自动答题系统是一款**开箱即用**的智能答题助手，集成了：
- 🖼️ **一键截图** - 快捷键快速截取题目
- 🔍 **离线OCR** - RapidOCR本地识别，无需联网，完全免费
- 🤖 **AI问答** - 支持DeepSeek/GPT/Claude等多种AI模型
- 📚 **历史记录** - 自动保存答题记录，随时回顾
- ⚙️ **高度可定制** - 快捷键、AI模型、主题等均可自定义

**完全开源，永久免费！**

---

## ✨ 功能特性

### 核心功能
- ✅ **智能OCR识别** - RapidOCR离线引擎，中英文混合识别准确率高
- ✅ **多AI支持** - DeepSeek（推荐）、OpenAI GPT、Claude、通义千问
- ✅ **快捷键操作** - 默认F9一键截图答题，可自定义
- ✅ **历史记录** - 自动保存最近100条答题记录
- ✅ **现代化界面** - 简洁美观的GUI设计

### 技术优势
- 🚀 **完全离线OCR** - 无需API密钥，无额度限制
- 💰 **超低成本** - DeepSeek API：1000道题仅需¥1
- 🔒 **隐私安全** - OCR本地处理，题目不上传
- 📦 **开箱即用** - 一键安装，简单配置即可使用
- 🎨 **高度可定制** - 支持自定义快捷键、AI模型、界面主题

---

## 🚀 快速开始

### 方法一：下载EXE（推荐）

1. 从 [Releases](https://github.com/dominciyue/Ai_OCR_answerauto/releases) 下载最新版本
2. 解压到任意目录
3. 双击运行 `AI答题系统.exe`
4. 首次启动配置AI密钥
5. 按F9开始使用！

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

## 🔑 API配置

### DeepSeek（推荐 - 性价比最高）

**为什么选择DeepSeek？**
- 💰 **超便宜**：输入¥1/百万tokens，输出¥2/百万tokens（GPT-4的1/30）
- 🎁 **新用户福利**：注册送500万tokens免费额度（约5000-10000道题）
- 🇨🇳 **国内友好**：支持国内手机号注册，支付宝/微信充值
- ⚡ **效果优秀**：媲美GPT-4的回答质量

**申请步骤（3分钟）：**
1. 访问 [DeepSeek平台](https://platform.deepseek.com/)
2. 注册账号（手机号/邮箱）
3. 创建API Key
4. 复制密钥到程序配置

📖 **详细教程**：[DeepSeek申请教程](docs/DeepSeek申请教程.md)

---

## 📸 使用演示

### 基本使用

1. **启动程序**

   ![启动界面](docs/images/main.png)

2. **按F9截图**

   ![截图](docs/images/capture.gif)

3. **查看答案**

   ![答案](docs/images/result.png)

### 高级功能

- **历史记录**：查看和复习之前的答题

  ![历史](docs/images/history.png)

- **快捷键设置**：自定义你喜欢的快捷键

  ![设置](docs/images/settings.png)

---

## 💡 使用技巧

### 截图技巧
- ✅ 尽量框选完整的题目（题干+选项）
- ✅ 确保文字清晰（打印体效果最佳）
- ✅ 避免截取多余内容（如水印、边框）
- ❌ 避免手写字（识别率较低）

### 费用说明

以DeepSeek为例：
- **免费额度**：新用户500万tokens ≈ 5000-10000道题
- **付费价格**：
  - 回答1道题 ≈ ¥0.001（一厘钱）
  - 回答100道题 ≈ ¥0.10（一毛钱）
  - 回答1000道题 ≈ ¥1（一块钱）

**极其便宜，放心使用！**

---

## 🛠️ 配置说明

### 自定义快捷键

点击主界面的"⚙️ 设置"按钮，可以修改：
- 快速答题快捷键（默认：F9）
- 退出程序快捷键（默认：Ctrl+Q）

### 切换AI模型

编辑 `config/config.yaml`：

```yaml
# DeepSeek
ai:
  provider: "openai"
  api_key: "sk-xxx"
  model: "deepseek-chat"
  base_url: "https://api.deepseek.com"

# OpenAI GPT
ai:
  provider: "openai"
  api_key: "sk-xxx"
  model: "gpt-4o"
  base_url: null

# Claude
ai:
  provider: "claude"
  api_key: "sk-ant-xxx"
  model: "claude-3-5-sonnet-20241022"
```

---

## 📚 文档

- [快速开始指南](docs/QUICKSTART.md)
- [DeepSeek申请教程](docs/DeepSeek申请教程.md)
- [API开发文档](docs/API.md)
- [常见问题FAQ](#常见问题)

---

## ❓ 常见问题

### Q: OCR识别不准确怎么办？
**A:** 
- 确保文字清晰（打印体最佳）
- 尽量截取完整题目
- 避免复杂背景

### Q: API调用失败？
**A:** 检查：
1. API Key是否正确
2. 网络连接是否正常
3. API余额是否充足

查看详细日志：`logs/app.log`

### Q: 快捷键冲突？
**A:** 点击"设置"按钮，修改为其他快捷键（如F10、F11）

### Q: 支持哪些AI模型？
**A:** 
- ✅ DeepSeek（推荐）
- ✅ OpenAI GPT-4/GPT-4o
- ✅ Claude 3.5 Sonnet
- ✅ 通义千问

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
- **AI**: DeepSeek / OpenAI / Claude
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

## 📊 项目统计

- 🌟 Star数：持续增长中
- 🔧 代码行数：约3500行
- 📦 项目大小：<20MB（打包后）
- ⚡ 启动速度：<3秒

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
