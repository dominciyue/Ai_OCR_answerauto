"""
OCR识别引擎
使用EasyOCR进行文字识别
"""

import os
import logging
from PIL import Image
import numpy as np

logger = logging.getLogger(__name__)


class OCREngine:
    """OCR识别引擎"""

    def __init__(self, config=None):
        self.config = config or {}
        self.ocr_config = self.config.get('ocr', {})
        self.ocr = None
        self._init_ocr()

    def _init_ocr(self):
        """初始化OCR引擎"""
        try:
            import easyocr

            # EasyOCR支持的语言代码
            lang = self.ocr_config.get('lang', 'ch')

            # 转换语言代码：ch -> ch_sim (简体中文), en -> en (英文)
            if lang == 'ch' or lang == 'ch_en':
                languages = ['ch_sim', 'en']  # 中英文混合
            elif lang == 'en':
                languages = ['en']
            else:
                languages = ['ch_sim', 'en']

            use_gpu = self.ocr_config.get('use_gpu', False)

            logger.info(f"正在初始化EasyOCR (语言: {languages}, GPU: {use_gpu})...")

            self.ocr = easyocr.Reader(
                languages,
                gpu=use_gpu,
                verbose=False
            )

            logger.info("EasyOCR初始化成功")

        except Exception as e:
            logger.error(f"EasyOCR初始化失败: {e}")
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
            result = self.ocr.readtext(img_array)

            if not result:
                logger.warning("未识别到任何文字")
                return ""

            # 提取文字和置信度
            confidence_threshold = self.ocr_config.get('confidence_threshold', 0.5)
            texts = []

            for detection in result:
                # EasyOCR返回格式: (bbox, text, confidence)
                bbox = detection[0]
                text = detection[1]
                confidence = detection[2]

                if confidence >= confidence_threshold:
                    texts.append(text)
                    logger.debug(f"识别: {text} (置信度: {confidence:.2f})")

            # 合并文字
            full_text = '\n'.join(texts)
            logger.info(f"OCR识别完成, 共 {len(texts)} 行文字")

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
            result = self.ocr.readtext(img_array)

            if not result:
                return []

            # 提取详细信息
            details = []
            for detection in result:
                bbox = detection[0]
                text = detection[1]
                confidence = detection[2]

                details.append({
                    'text': text,
                    'box': bbox,
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
            'lang': 'ch',
            'use_gpu': False,
            'confidence_threshold': 0.5
        }
    }

    engine = OCREngine(test_config)
    print("OCR引擎初始化成功！")
