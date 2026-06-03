"""
AI客户端模块 - 支持多种国产大模型
"""

import logging
from openai import OpenAI
import anthropic

logger = logging.getLogger(__name__)


# 国产大模型配置
DOMESTIC_MODELS = {
    'deepseek': {
        'name': 'DeepSeek',
        'base_url': 'https://api.deepseek.com',
        'model': 'deepseek-chat',
        'provider': 'openai',
        'description': '推荐 - 性价比最高，新用户送500万tokens'
    },
    'qwen': {
        'name': '通义千问',
        'base_url': 'https://dashscope.aliyuncs.com/compatible-mode/v1',
        'model': 'qwen-turbo',
        'provider': 'openai',
        'description': '阿里云出品，速度快'
    },
    'zhipu': {
        'name': '智谱AI',
        'base_url': 'https://open.bigmodel.cn/api/paas/v4',
        'model': 'glm-4-flash',
        'provider': 'openai',
        'description': '清华出品，效果好'
    },
    'moonshot': {
        'name': 'Moonshot',
        'base_url': 'https://api.moonshot.cn/v1',
        'model': 'moonshot-v1-8k',
        'provider': 'openai',
        'description': 'Kimi出品，上下文长'
    },
    'baichuan': {
        'name': '百川智能',
        'base_url': 'https://api.baichuan-ai.com/v1',
        'model': 'Baichuan2-Turbo',
        'provider': 'openai',
        'description': '百川出品，性能稳定'
    },
    'doubao': {
        'name': '豆包',
        'base_url': 'https://ark.cn-beijing.volces.com/api/v3',
        'model': 'doubao-pro-4k',
        'provider': 'openai',
        'description': '字节跳动出品'
    }
}


class AIClient:
    """AI客户端"""

    def __init__(self, config):
        self.config = config
        self.ai_config = config.get('ai', {})
        self.client = None
        self._init_client()

    def _init_client(self):
        """初始化AI客户端"""
        provider = self.ai_config.get('provider', 'openai')
        api_key = self.ai_config.get('api_key')
        model = self.ai_config.get('model')

        if not api_key:
            raise ValueError("API密钥未配置")

        logger.info(f"初始化AI客户端: {provider}, 模型: {model}")

        try:
            if provider == 'openai':
                # 支持OpenAI兼容的API（DeepSeek、通义千问等）
                base_url = self.ai_config.get('base_url')
                self.client = OpenAI(
                    api_key=api_key,
                    base_url=base_url,
                    timeout=self.ai_config.get('timeout', 30),
                    max_retries=self.ai_config.get('max_retries', 3)
                )
            elif provider == 'claude':
                # Claude
                self.client = anthropic.Anthropic(
                    api_key=api_key,
                    timeout=self.ai_config.get('timeout', 30),
                    max_retries=self.ai_config.get('max_retries', 3)
                )
            else:
                raise ValueError(f"不支持的AI提供商: {provider}")

            logger.info("AI客户端初始化成功")

        except Exception as e:
            logger.error(f"AI客户端初始化失败: {e}")
            raise

    def answer_question(self, question_text):
        """
        回答问题

        Args:
            question_text: 题目文本

        Returns:
            str: AI的回答
        """
        if not question_text or not question_text.strip():
            return None

        provider = self.ai_config.get('provider', 'openai')
        model = self.ai_config.get('model')

        system_prompt = """你是一个专业的答题助手。请分析题目并给出：
1. 题目类型（单选/多选/判断/填空/简答）
2. 正确答案
3. 详细解析

要求：
- 答案准确
- 解析清晰
- 语言简洁
"""

        try:
            logger.info("正在请求AI回答问题...")

            if provider == 'openai':
                response = self.client.chat.completions.create(
                    model=model,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": question_text}
                    ],
                    temperature=0.3,
                    max_tokens=1000
                )
                answer = response.choices[0].message.content

            elif provider == 'claude':
                response = self.client.messages.create(
                    model=model,
                    max_tokens=1000,
                    temperature=0.3,
                    system=system_prompt,
                    messages=[
                        {"role": "user", "content": question_text}
                    ]
                )
                answer = response.content[0].text

            else:
                return None

            logger.info("AI回答成功")
            return answer

        except Exception as e:
            logger.error(f"AI回答失败: {e}")
            raise


def get_domestic_models():
    """获取国产大模型列表"""
    return DOMESTIC_MODELS


# 测试代码
if __name__ == "__main__":
    import sys
    import yaml

    logging.basicConfig(level=logging.INFO)

    # 加载配置
    with open('../config/config.yaml', 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f)

    # 测试
    client = AIClient(config)
    test_question = "1+1等于几？"

    print(f"问题: {test_question}")
    answer = client.answer_question(test_question)
    print(f"回答: {answer}")
