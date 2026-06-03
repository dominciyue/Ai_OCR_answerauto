# AI自动答题系统 - API文档

本文档说明如何将AI答题系统作为API服务使用。

## 概述

AI答题系统提供两种使用方式：
1. **桌面应用** - 双击运行，直接使用（已完成）
2. **API服务** - 通过HTTP接口调用（待开发）

---

## API服务架构设计

### 方案一：本地API服务（推荐）

```
用户应用 (你的程序)
    ↓ HTTP请求
本地API服务 (localhost:8000)
    ↓
AI答题系统核心
    ├→ OCR识别
    └→ AI问答
```

**优点：**
- 轻量级，易部署
- 数据本地处理，安全
- 无需网络部署

### 方案二：云端API服务

```
用户应用
    ↓ HTTPS
云端API服务器
    ├→ 免费额度管理
    ├→ 用户认证
    └→ AI答题服务
```

**优点：**
- 提供免费额度
- 多用户管理
- 无需本地安装

---

## API接口设计

### 1. 文字识别接口

**请求：**
```http
POST /api/ocr
Content-Type: multipart/form-data

image: <图片文件>
```

**响应：**
```json
{
  "code": 0,
  "message": "success",
  "data": {
    "text": "识别出的题目文本",
    "confidence": 0.95
  }
}
```

### 2. AI问答接口

**请求：**
```http
POST /api/answer
Content-Type: application/json

{
  "question": "题目内容",
  "model": "deepseek-chat"  // 可选
}
```

**响应：**
```json
{
  "code": 0,
  "message": "success",
  "data": {
    "answer": "AI回答内容",
    "question_type": "单选",
    "explanation": "解析内容"
  }
}
```

### 3. 完整识别接口（OCR + AI）

**请求：**
```http
POST /api/recognize
Content-Type: multipart/form-data

image: <图片文件>
model: "deepseek-chat"  // 可选
```

**响应：**
```json
{
  "code": 0,
  "message": "success",
  "data": {
    "question": "识别的题目",
    "answer": "AI回答",
    "question_type": "单选",
    "explanation": "解析"
  }
}
```

---

## 实现方案

### 本地API服务实现（FastAPI）

创建 `api_server.py`:

```python
from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import JSONResponse
from PIL import Image
import io
import yaml

# 导入核心模块
from src.ocr_engine import OCREngine
from src.ai_client import AIClient

app = FastAPI(title="AI答题系统API")

# 初始化
def load_config():
    with open('config/config.yaml', 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

config = load_config()
ocr_engine = OCREngine(config)
ai_client = AIClient(config)

@app.post("/api/ocr")
async def ocr_recognize(image: UploadFile = File(...)):
    """OCR识别接口"""
    try:
        # 读取图片
        image_data = await image.read()
        img = Image.open(io.BytesIO(image_data))
        
        # OCR识别
        text = ocr_engine.recognize(img)
        
        return JSONResponse({
            "code": 0,
            "message": "success",
            "data": {
                "text": text,
                "confidence": 0.95
            }
        })
    except Exception as e:
        return JSONResponse({
            "code": 1,
            "message": str(e)
        }, status_code=500)

@app.post("/api/answer")
async def ai_answer(question: str = Form(...)):
    """AI问答接口"""
    try:
        answer = ai_client.answer_question(question)
        
        return JSONResponse({
            "code": 0,
            "message": "success",
            "data": {
                "answer": answer
            }
        })
    except Exception as e:
        return JSONResponse({
            "code": 1,
            "message": str(e)
        }, status_code=500)

@app.post("/api/recognize")
async def full_recognize(image: UploadFile = File(...)):
    """完整识别接口（OCR + AI）"""
    try:
        # OCR识别
        image_data = await image.read()
        img = Image.open(io.BytesIO(image_data))
        question = ocr_engine.recognize(img)
        
        # AI回答
        answer = ai_client.answer_question(question)
        
        return JSONResponse({
            "code": 0,
            "message": "success",
            "data": {
                "question": question,
                "answer": answer
            }
        })
    except Exception as e:
        return JSONResponse({
            "code": 1,
            "message": str(e)
        }, status_code=500)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

启动：
```bash
pip install fastapi uvicorn python-multipart
python api_server.py
```

---

## 使用示例

### Python调用示例

```python
import requests

# OCR识别
with open('question.png', 'rb') as f:
    response = requests.post(
        'http://localhost:8000/api/ocr',
        files={'image': f}
    )
    print(response.json())

# AI问答
response = requests.post(
    'http://localhost:8000/api/answer',
    data={'question': '什么是Python？'}
)
print(response.json())

# 完整识别
with open('question.png', 'rb') as f:
    response = requests.post(
        'http://localhost:8000/api/recognize',
        files={'image': f}
    )
    print(response.json())
```

### JavaScript调用示例

```javascript
// 完整识别
const formData = new FormData();
formData.append('image', fileInput.files[0]);

fetch('http://localhost:8000/api/recognize', {
    method: 'POST',
    body: formData
})
.then(res => res.json())
.then(data => {
    console.log('题目:', data.data.question);
    console.log('答案:', data.data.answer);
});
```

---

## 下一步开发

如果你需要API服务，我可以帮你：

1. **实现本地API服务**（上面的代码）
2. **实现云端API服务**（带免费额度管理）
3. **添加用户认证和额度控制**
4. **提供SDK封装**（Python、JavaScript等）

你想要哪种方案？
