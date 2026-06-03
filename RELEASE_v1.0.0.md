# v1.0.0 Release Notes

## 🎉 首次发布

AI自动答题系统 v1.0.0 正式发布！

### ✨ 核心功能

- **一键截图** - 按F9快速截取题目（可自定义）
- **智能OCR** - RapidOCR离线引擎，中英文混合识别
- **AI问答** - 支持DeepSeek/OpenAI GPT/Claude等模型
- **历史记录** - 自动保存最近100条答题记录
- **快捷键设置** - 可视化设置界面，自定义快捷键
- **现代化GUI** - 绿色主题，卡片式设计

### 💡 技术亮点

- ✅ **完全离线OCR** - RapidOCR本地处理，无需API，无额度限制
- ✅ **超低成本** - DeepSeek API：1000道题仅需¥1
- ✅ **隐私安全** - OCR本地识别，题目内容不上传
- ✅ **开箱即用** - 简单配置即可使用
- ✅ **完全开源** - MIT协议，永久免费

### 📦 下载安装

#### Windows用户（推荐）
1. 下载 `AI答题系统_v1.0.0_Windows.zip`
2. 解压到任意目录
3. 运行 `AI答题系统.exe`
4. 首次启动配置DeepSeek API Key
5. 按F9开始使用

#### 从源码运行
```bash
git clone https://github.com/dominciyue/Ai_OCR_answerauto.git
cd Ai_OCR_answerauto
pip install -r requirements.txt
python src/main.py
```

### 🔑 获取API Key

**推荐使用DeepSeek（性价比最高）：**

1. 访问 [DeepSeek平台](https://platform.deepseek.com/)
2. 注册账号（国内手机号即可）
3. 创建API Key
4. 新用户送500万tokens免费额度（约5000-10000道题）

详细教程：[DeepSeek申请教程](docs/DeepSeek申请教程.md)

### 📊 使用成本

- **免费额度**：新用户500万tokens ≈ 5000-10000道题
- **付费价格**（用完免费额度后）：
  - 1道题 ≈ ¥0.001（一厘钱）
  - 100道题 ≈ ¥0.10（一毛钱）
  - 1000道题 ≈ ¥1（一块钱）

**极其便宜，放心使用！**

### 🎯 使用场景

- ✏️ 学习辅助 - 理解题目解题思路
- 📝 作业帮助 - 快速获取答案和解析
- 🎓 知识巩固 - 查看详细解题步骤
- 💡 思路启发 - AI分析题目类型和考点

### ⚠️ 免责声明

本工具仅供学习研究使用，请遵守学术诚信政策。不当使用造成的后果由使用者自行承担。

### 🐛 已知问题

- Windows DPI缩放可能影响截图显示（已修复）
- 托盘图标需要安装pystray（可选功能）

### 📝 更新日志

- ✨ 首次发布
- 🎨 现代化GUI界面
- 🔧 支持自定义快捷键
- 📚 完整的中文文档
- 🚀 开箱即用的配置向导

### 🙏 致谢

- [RapidOCR](https://github.com/RapidAI/RapidOCR) - 优秀的离线OCR引擎
- [DeepSeek](https://www.deepseek.com/) - 高性价比的AI服务
- 所有贡献者和使用者

### 📞 反馈与支持

- 🐛 [报告Bug](https://github.com/dominciyue/Ai_OCR_answerauto/issues)
- 💬 [讨论交流](https://github.com/dominciyue/Ai_OCR_answerauto/discussions)
- ⭐ 如果觉得有帮助，请点个Star！

---

**Made with ❤️ by [dominciyue](https://github.com/dominciyue)**
