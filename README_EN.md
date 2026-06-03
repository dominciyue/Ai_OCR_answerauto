# AI Auto Answer System

An open-source intelligent answer assistant that automatically recognizes questions on screen and retrieves answers through AI.

## Features

- 🖼️ **Screen Capture** - Full screen or region capture
- 🔍 **Smart OCR** - Chinese and English text recognition based on PaddleOCR
- 🤖 **AI Q&A** - Supports multiple AI models (OpenAI GPT, Claude, Qwen)
- ⚡ **Hotkey Support** - Quick launch (default F9)
- 💬 **Real-time Feedback** - Floating window displays answers
- 🔧 **Flexible Configuration** - Customizable API and parameters

## Quick Start

### Installation

```bash
pip install -r requirements.txt
```

### Configuration

Edit `config/config.yaml` and fill in your API key:

```yaml
ai:
  provider: "openai"  # openai, claude, or qwen
  api_key: "your-api-key-here"
  model: "gpt-4o"
```

### Run

```bash
python src/main.py
```

## Usage

1. Press **F9** to start capture
2. Drag mouse to select question area
3. Wait for OCR recognition and AI analysis
4. Answer will be displayed in floating window

## Documentation

- [Quick Start Guide](docs/QUICKSTART.md)
- [Architecture](docs/ARCHITECTURE.md)
- [中文文档](README.md)

## Tech Stack

- **OCR**: PaddleOCR
- **AI**: OpenAI API / Anthropic Claude / Alibaba Qwen
- **GUI**: Tkinter
- **Capture**: Pillow, mss
- **Hotkey**: keyboard

## Disclaimer

⚠️ This tool is for learning and technical research purposes only. Please comply with your school/institution's academic integrity policies. Users are responsible for any consequences of improper use.

## License

MIT License - See [LICENSE](LICENSE) file

---

**Made with ❤️ for learners**
