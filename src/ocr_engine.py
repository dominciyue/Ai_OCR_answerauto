"""
OCR识别引擎 - 使用RapidOCR（离线OCR）
完全免费，无需API密钥，适合开源项目
"""

import logging
from PIL import Image
import numpy as np

logger = logging.getLogger(__name__)


class OCREngine:
    """OCR识别引擎 - RapidOCR"""

    def __init__(self, config=None):
        self.config = config or {}
        self.ocr_config = self.config.get('ocr', {})
        self.ocr = None
        self._init_ocr()

    def _init_ocr(self):
        """初始化OCR引擎"""
        try:
            from rapidocr_onnxruntime import RapidOCR

            logger.info("正在初始化RapidOCR（离线OCR引擎）...")

            # 初始化RapidOCR
            self.ocr = RapidOCR()

            logger.info("RapidOCR初始化成功")

        except ImportError:
            logger.error("RapidOCR未安装，请运行: pip install rapidocr-onnxruntime")
            raise Exception("RapidOCR未安装，请运行: pip install rapidocr-onnxruntime")
        except Exception as e:
            logger.error(f"OCR初始化失败: {e}")
            raise

    def recognize(self, image):
        """
        识别图片中的文字

        Args:
            image: PIL Image对象

        Returns:
            str: 识别出的文字内容
        """
        if not self.ocr:
            raise RuntimeError("OCR引擎未初始化")

        try:
            # 转换为numpy数组
            if isinstance(image, Image.Image):
                img_array = np.array(image)
            else:
                img_array = image

            logger.info(f"开始OCR识别, 图片大小: {img_array.shape}")

            # 执行识别
            result, elapse = self.ocr(img_array)

            if not result or len(result) == 0:
                logger.warning("未识别到任何文字")
                return ""

            # 提取文字和置信度
            confidence_threshold = self.ocr_config.get('confidence_threshold', 0.5)
            texts = []

            for line in result:
                # RapidOCR返回格式: [[box], text, confidence]
                if line and len(line) >= 3:
                    box = line[0]  # 文字框坐标
                    text = line[1]  # 文字内容
                    confidence = line[2]  # 置信度

                    if confidence >= confidence_threshold:
                        texts.append(text)
                        logger.debug(f"识别: {text} (置信度: {confidence:.2f})")

            # 合并文字
            full_text = '\n'.join(texts)

            # elapse可能是列表或数字
            elapse_time = sum(elapse) if isinstance(elapse, list) else elapse
            logger.info(f"OCR识别完成, 共 {len(texts)} 行文字, 耗时: {elapse_time:.2f}秒")

            return full_text

        except Exception as e:
            logger.error(f"OCR识别失败: {e}")
            raise

    def recognize_with_details(self, image):
        """
        识别图片中的文字（包含详细信息）

        Returns:
            list: 包含文字、位置、置信度的列表
        """
        if not self.ocr:
            raise RuntimeError("OCR引擎未初始化")

        try:
            # 转换为numpy数组
            if isinstance(image, Image.Image):
                img_array = np.array(image)
            else:
                img_array = image

            # 执行识别
            result, elapse = self.ocr(img_array)

            if not result or len(result) == 0:
                return []

            # 提取详细信息
            details = []
            for line in result:
                if line and len(line) >= 3:
                    box = line[0]
                    text = line[1]
                    confidence = line[2]

                    details.append({
                        'text': text,
                        'box': box,
                        'confidence': confidence
                    })

            return details

        except Exception as e:
            logger.error(f"OCR识别失败: {e}")
            raise


# 测试代码
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    # 测试OCR
    test_config = {
        'ocr': {
            'confidence_threshold': 0.5
        }
    }

    try:
        engine = OCREngine(test_config)
        print("OCR引擎初始化成功！")

        # 测试识别
        from PIL import Image
        test_image = Image.new('RGB', (100, 100), color='white')
        result = engine.recognize(test_image)
        print(f"识别结果: {result}")

    except Exception as e:
        print(f"错误: {e}")
