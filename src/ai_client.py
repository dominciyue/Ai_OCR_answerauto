"""
AI客户端模块
支持多种AI API: OpenAI, Claude, 通义千问
"""

import logging
import time
from typing import Optional

logger = logging.getLogger(__name__)


class AIClient:
    """AI客户端统一接口"""

    def __init__(self, config):
        self.config = config
        self.ai_config = config.get('ai', {})
        self.provider = self.ai_config.get('provider', 'openai').lower()
        self.api_key = self.ai_config.get('api_key')
        self.model = self.ai_config.get('model')
        self.base_url = self.ai_config.get('base_url')
        self.timeout = self.ai_config.get('timeout', 30)
        self.max_retries = self.ai_config.get('max_retries', 3)

        self.client = None
        self._init_client()

    def _init_client(self):
        """初始化AI客户端"""
        logger.info(f"初始化AI客户端: {self.provider}, 模型: {self.model}")

        try:
            if self.provider == 'openai':
                self._init_openai()
            elif self.provider == 'claude':
                self._init_claude()
            elif self.provider == 'qwen':
                self._init_qwen()
            else:
                raise ValueError(f"不支持的AI提供商: {self.provider}")

            logger.info("AI客户端初始化成功")

        except Exception as e:
            logger.error(f"AI客户端初始化失败: {e}")
            raise

    def _init_openai(self):
        """初始化OpenAI客户端"""
        from openai import OpenAI

        kwargs = {
            'api_key': self.api_key,
            'timeout': self.timeout,
        }

        if self.base_url:
            kwargs['base_url'] = self.base_url

        self.client = OpenAI(**kwargs)

    def _init_claude(self):
        """初始化Claude客户端"""
        from anthropic import Anthropic

        kwargs = {
            'api_key': self.api_key,
            'timeout': self.timeout,
        }

        if self.base_url:
            kwargs['base_url'] = self.base_url

        self.client = Anthropic(**kwargs)

    def _init_qwen(self):
        """初始化通义千问客户端"""
        from openai import OpenAI

        # 通义千问兼容OpenAI接口
        self.client = OpenAI(
            api_key=self.api_key,
            base_url=self.base_url or "https://dashscope.aliyuncs.com/compatible-mode/v1",
            timeout=self.timeout,
        )

    def answer_question(self, question_text: str) -> Optional[str]:
        """
        根据题目获取答案

        Args:
            question_text: 题目文本

        Returns:
            str: AI生成的答案
        """
        if not question_text or not question_text.strip():
            logger.warning("题目文本为空")
            return None

        logger.info(f"正在请求AI回答问题...")
        logger.debug(f"题目内容: {question_text[:100]}...")

        # 构建提示词
        prompt = self._build_prompt(question_text)

        # 重试逻辑
        for attempt in range(1, self.max_retries + 1):
            try:
                if self.provider == 'claude':
                    answer = self._call_claude(prompt)
                else:
                    answer = self._call_openai_compatible(prompt)

                logger.info("AI回答成功")
                return answer

            except Exception as e:
                logger.warning(f"第 {attempt} 次尝试失败: {e}")

                if attempt < self.max_retries:
                    wait_time = 2 ** attempt  # 指数退避
                    logger.info(f"等待 {wait_time} 秒后重试...")
                    time.sleep(wait_time)
                else:
                    logger.error("达到最大重试次数，请求失败")
                    raise

        return None

    def _build_prompt(self, question_text: str) -> str:
        """构建提示词"""
        prompt = f"""你是一个专业的答题助手。请仔细分析以下题目，并给出准确、详细的答案。

题目内容：
{question_text}

请按以下格式回答：

1. **题目类型**：（单选/多选/判断/填空/简答等）

2. **答案**：
   [在这里给出明确的答案]

3. **解析**：
   [简要说明答题思路和关键知识点]

注意：
- 如果是选择题，请给出选项字母和完整内容
- 如果题目不完整或无法理解，请说明原因
- 保持回答简洁明了，重点突出
"""
        return prompt

    def _call_openai_compatible(self, prompt: str) -> str:
        """调用OpenAI兼容的API"""
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "system",
                    "content": "你是一个专业、准确的答题助手。"
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.3,  # 降低随机性，提高准确性
            max_tokens=2000,
        )

        answer = response.choices[0].message.content.strip()
        return answer

    def _call_claude(self, prompt: str) -> str:
        """调用Claude API"""
        response = self.client.messages.create(
            model=self.model,
            max_tokens=2000,
            temperature=0.3,
            system="你是一个专业、准确的答题助手。",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        answer = response.content[0].text.strip()
        return answer


# 测试代码
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    # 测试配置
    test_config = {
        'ai': {
            'provider': 'openai',
            'api_key': 'test-key',
            'model': 'gpt-4o',
            'timeout': 30,
            'max_retries': 3
        }
    }

    try:
        client = AIClient(test_config)
        print("AI客户端初始化成功！")

        # 测试问题
        test_question = """
        1. 以下哪项是Python的特点？
        A. 静态类型
        B. 动态类型
        C. 编译型语言
        D. 不支持面向对象
        """

        # answer = client.answer_question(test_question)
        # print(f"\n答案：\n{answer}")

    except Exception as e:
        print(f"测试失败: {e}")
