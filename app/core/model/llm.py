
import os
import logging
from functools import lru_cache
from typing import Optional

from dotenv import load_dotenv

load_dotenv()
logger = logging.getLogger(__name__)

_API_KEY: Optional[str] = None


def _get_api_key() -> str:
    global _API_KEY
    if _API_KEY is None:
        _API_KEY = os.getenv("API_KEY", "")
        if not _API_KEY:
            raise RuntimeError("环境变量 API_KEY 未配置")
    return _API_KEY


@lru_cache(maxsize=4)
def get_chat_model(model_name: str = "qwen-plus", streaming: bool = False):
    from langchain_community.chat_models.tongyi import ChatTongyi

    logger.info("初始化 ChatTongyi: model=%s, streaming=%s", model_name, streaming)
    return ChatTongyi(model=model_name, api_key=_get_api_key(), streaming=streaming)


def get_streaming_model(model_name: str = "qwen-plus"):
    return get_chat_model(model_name, streaming=True)


def call_image_synthesis(prompt: str, model_name: str = "wanx-v1"):
    import dashscope
    from app.core.plan.sys_TextToImage_prompt import SYS_TEXT_TO_IMAGE_PROMPT

    logger.info("调用图像合成: model=%s", model_name)
    return dashscope.ImageSynthesis.call(
        model=model_name,
        api_key=_get_api_key(),
        prompt=prompt or SYS_TEXT_TO_IMAGE_PROMPT,
        size="1024*1024",
        n=1,
        response_format="url",
    )
