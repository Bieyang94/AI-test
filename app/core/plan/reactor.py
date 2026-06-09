
import base64
import logging
import os
from typing import Generator, AsyncGenerator

import dashscope
import requests
from langchain.agents import create_agent
from langchain.tools import tool

from app.core.model.llm import get_streaming_model, _get_api_key, call_image_synthesis
from app.core.plan.sys_prompt import (
    SYS_REQUIREMENT_ANALYZE_PROMPT,
    SYS_GENERATE_TESTPOINT_PROMPT,
    SYS_GENERATE_TESTSAMPLE_PROMPT,
)
from app.core.plan.sys_TextToImage_prompt import SYS_TEXT_TO_IMAGE_PLAN_PROMPT

logger = logging.getLogger(__name__)


class BaseStreamAgent:
    """公共基类：提供流式输出能力"""

    def __init__(self, system_prompt: str, agent_tools=None, model_name: str = "qwen-plus"):
        self.system_prompt = system_prompt
        self._model_name = model_name
        self._agent = None
        self._agent_tools = agent_tools

    @property
    def agent(self):
        if self._agent is None:
            model = get_streaming_model(self._model_name)
            self._agent = create_agent(
                model=model,
                system_prompt=self.system_prompt,
                tools=self._agent_tools,
            )
        return self._agent

    def _stream_chunks(self, input_dict: dict) -> Generator[str, None, None]:
        for chunk in self.agent.stream(input_dict, stream_mode="values", context={"report": False}):
            if "messages" not in chunk:
                continue
            latest_message = chunk["messages"][-1]
            if hasattr(latest_message, "type") and latest_message.type != "ai":
                continue
            content = latest_message.content
            if content and content.strip():
                yield content.strip()

    def execute_stream(self, msg_user: str) -> str:
        input_dict = {"messages": [{"role": "user", "content": msg_user}]}
        parts = list(self._stream_chunks(input_dict))
        return "".join(parts)

    def execute_stream_generator(self, msg_user: str) -> Generator[str, None, None]:
        input_dict = {"messages": [{"role": "user", "content": msg_user}]}
        yield from self._stream_chunks(input_dict)

    def stream_tokens(self, msg_user: str) -> Generator[str, None, None]:
        try:
            responses = dashscope.Generation.call(
                model=self._model_name,
                api_key=_get_api_key(),
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": msg_user},
                ],
                result_format="message",
                stream=True,
                incremental_output=True,
            )
            for response in responses:
                if response.status_code == 200:
                    content = response.output.choices[0].message.content
                    if content:
                        yield content
                else:
                    raise RuntimeError(
                        f"DashScope 流式调用失败: {response.code} - {response.message}"
                    )
        except GeneratorExit:
            return
        except Exception as e:
            if "StopIteration" in type(e).__name__ or "Future" in str(e):
                return
            raise

    async def astream_tokens(self, msg_user: str) -> AsyncGenerator[str, None]:
        import asyncio

        _SENTINEL = object()

        def _safe_next(gen):
            try:
                return next(gen)
            except StopIteration:
                return _SENTINEL

        loop = asyncio.get_event_loop()
        gen = self.stream_tokens(msg_user)

        while True:
            chunk = await loop.run_in_executor(None, _safe_next, gen)
            if chunk is _SENTINEL:
                break
            yield chunk
            await asyncio.sleep(0)


@tool
def text_to_image(prompt: str) -> str:
    """根据用户的文本提示词生成图片，返回图片URL和Base64编码"""
    result = call_image_synthesis(prompt)
    if result.status_code == 200:
        image_url = result.output.results[0]["url"]
        resp = requests.get(image_url, timeout=30)
        resp.raise_for_status()
        image_base64 = base64.b64encode(resp.content).decode("utf-8")
        return f"图片生成成功\n{image_url}\n{image_base64[:200]}..."
    return f"绘图失败:{result.message}"


class ReactAgent(BaseStreamAgent):
    def __init__(self):
        super().__init__(system_prompt=SYS_GENERATE_TESTSAMPLE_PROMPT)


class XmindReactorAgent(BaseStreamAgent):
    def __init__(self):
        super().__init__(
            system_prompt=SYS_TEXT_TO_IMAGE_PLAN_PROMPT,
            agent_tools=[text_to_image],
        )


class ExtractTitleAgent(BaseStreamAgent):
    def __init__(self):
        super().__init__(system_prompt=SYS_REQUIREMENT_ANALYZE_PROMPT)


class GenerateTestPointAgent(BaseStreamAgent):
    def __init__(self):
        super().__init__(system_prompt=SYS_GENERATE_TESTPOINT_PROMPT)


# 向后兼容别名
extract_title_ReactorAgent = ExtractTitleAgent
generate_testPoint_ReactorAgent = GenerateTestPointAgent
requirement_analyze_ReactorAgent = ExtractTitleAgent
