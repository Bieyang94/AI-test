"""
根据输入的markdown，word，pdf生成测试用例和思维导图
"""

from app.core.plan import reactor
from app.core.tools import extract_word
from app.core.tools import extract_mdToheader
from app.core.tools import extract_pdf
from app.core.data_transformer import markdown_to_csv
import io
from typing import List, Dict, Any, Union

generateTestPoint = reactor.generate_testPoint_ReactorAgent()


#markdown

class agent_output_markdown:
    def __init__(self, user_input: str):
        self.user_input = user_input

    def generate_title(self):
        content = self.user_input
        requirement_md = extract_mdToheader.generate_requirement_by_model(content)
        return requirement_md

    def generate_title_stream(self):
        """同步流式（Streamlit 用）"""
        requirement_agent = reactor.extract_title_ReactorAgent()
        yield from requirement_agent.stream_tokens(self.user_input)

    async def agenerate_title_stream(self):
        """异步流式（FastAPI StreamingResponse 用）"""
        requirement_agent = reactor.extract_title_ReactorAgent()
        async for chunk in requirement_agent.astream_tokens(self.user_input):
            yield chunk

    async def generate_xmind(self, outline: str = None):
        """生成 xmind + 功能点文本（FastAPI 用）"""
        requirement_md = outline or self.user_input
        test_point_md = await generateTestPoint.agent.ainvoke({
            "messages": [
                {"role": "user", "content": requirement_md}
            ]
        })
        test_points_str = test_point_md["messages"][-1].content
        xmind_md = extract_mdToheader.markdown_to_xmind(
            content=test_points_str,
            sheet_title="md思维导图"
        )
        return {
            "xmind_bytes": xmind_md["xmind_bytes"],
            "test_points": test_points_str,
        }

    def generate_csv(self, test_points: str = None):
        """根据功能点文本生成 CSV（可直接传入缓存的 test_points）"""
        function_point_md = test_points or self.user_input
        csv_str = markdown_to_csv.generate_testcase_csv(function_point_md)
        return csv_str

#docx

class agent_output_docx:
    def __init__(self, word_source: Union[str, bytes, io.BytesIO]):
        self.path = word_source

    def generate_title(self):
        requirement_docx = extract_word.generate_title_by_model(self.path)
        return requirement_docx

    def generate_title_stream(self):
        """同步流式（Streamlit 用）"""
        raw_text = extract_word.extract_text_only(self.path)
        requirement_agent = reactor.extract_title_ReactorAgent()
        yield from requirement_agent.stream_tokens(raw_text)

    async def agenerate_title_stream(self):
        """异步流式（FastAPI 用）"""
        raw_text = extract_word.extract_text_only(self.path)
        requirement_agent = reactor.extract_title_ReactorAgent()
        async for chunk in requirement_agent.astream_tokens(raw_text):
            yield chunk

    async def generate_xmind(self, outline: str = None):
        requirement_md = outline or extract_word.generate_title_by_model(self.path)
        test_point_md = await generateTestPoint.agent.ainvoke({
            "messages": [
                {"role": "user", "content": requirement_md}
            ]
        })
        test_points_str = test_point_md["messages"][-1].content
        xmind_docx = extract_mdToheader.markdown_to_xmind(
            content=test_points_str,
            sheet_title="word思维导图"
        )
        return {
            "xmind_bytes": xmind_docx["xmind_bytes"],
            "test_points": test_points_str,
        }

    def generate_csv(self, test_points: str = None):
        if test_points is None:
            requirement_docx = extract_word.generate_title_by_model(self.path)
            test_point_docx = generateTestPoint.agent.invoke({
                "messages": [{"role": "user", "content": requirement_docx}]
            })
            test_points = test_point_docx["messages"][-1].content
        csv_str = markdown_to_csv.generate_testcase_csv(test_points)
        return csv_str

#pdf

class agent_output_pdf:
    def __init__(self, pdf_source: Union[str, bytes, io.BytesIO]):
        self.path = pdf_source

    def generate_title(self):
        content = extract_pdf.generate_title_by_model(self.path)
        return content

    def generate_title_stream(self):
        """同步流式（Streamlit 用）"""
        raw_text = extract_pdf.extract_text_only(self.path)
        requirement_agent = reactor.extract_title_ReactorAgent()
        yield from requirement_agent.stream_tokens(raw_text)

    async def agenerate_title_stream(self):
        """异步流式（FastAPI 用）"""
        raw_text = extract_pdf.extract_text_only(self.path)
        requirement_agent = reactor.extract_title_ReactorAgent()
        async for chunk in requirement_agent.astream_tokens(raw_text):
            yield chunk

    async def generate_xmind(self, outline: str = None):
        requirement_md = outline or extract_pdf.generate_title_by_model(self.path)
        test_point_md = await generateTestPoint.agent.ainvoke({
            "messages": [
                {"role": "user", "content": requirement_md}
            ]
        })
        test_points_str = test_point_md["messages"][-1].content
        xmind_pdf = extract_mdToheader.markdown_to_xmind(
            content=test_points_str,
            sheet_title="pdf思维导图"
        )
        return {
            "xmind_bytes": xmind_pdf["xmind_bytes"],
            "test_points": test_points_str,
        }

    def generate_csv(self, test_points: str = None):
        if test_points is None:
            requirement_pdf = extract_pdf.generate_title_by_model(self.path)
            test_point_pdf = generateTestPoint.agent.invoke({
                "messages": [{"role": "user", "content": requirement_pdf}]
            })
            test_points = test_point_pdf["messages"][-1].content
        csv_str = markdown_to_csv.generate_testcase_csv(test_points)
        return csv_str

if __name__ == "__main__":
    # #markdown
    # agentOutputMarkdown = agent_output_markdown(reactor.function_requiremen.question)
    # markdown_title = agentOutputMarkdown.generate_title()
    # print(markdown_title)
    # print("=" * 50)
    # test_point_md = generateTestPoint.agent.invoke({
    #     "messages": [
    #         {"role": "user", "content": markdown_title}
    #     ]
    # })
    # print(test_point_md["messages"][-1].content)
    # print("=" * 50)
    # xmind_bin = agentOutputMarkdown.generate_xmind()
    # print(f"\n📦 已生成内存二进制，大小：{len(xmind_bin)} 字节")
    # print("=" * 50)
    # markdown_csv = agentOutputMarkdown.generate_csv()
    # print(markdown_csv)

    #docx
    # path = r"C:\Users\EDY\Desktop\掘金2.0产品需求文档 .docx"
    # with open(path, "rb") as f:
    #     docx_bytes = f.read()  # 拿到 docx 二进制
    # agentOutputdocx = agent_output_docx(docx_bytes)
    # docx_title = agentOutputdocx.generate_title()
    # print(docx_title)
    # print("=" * 50)
    # test_point_md = generateTestPoint.agent.invoke({
    #     "messages": [
    #         {"role": "user", "content": docx_title}
    #     ]
    # })
    # print("=" * 50)
    # print(test_point_md["messages"][-1].content)
    # xmind_bin = agentOutputdocx.generate_xmind()
    # print(f"\n📦 已生成内存二进制，大小：{len(xmind_bin)} 字节")
    # docx_csv = agentOutputdocx.generate_csv()
    # print(docx_csv)

    #pdf
    path = r"C:\Users\EDY\Desktop\掘金2.0产品需求文档 .pdf"
    with open(path, "rb") as f:
        pdf_bytes = f.read()  # 拿到 PDF 二进制

    agentOutputPdf = agent_output_pdf(pdf_bytes)
    pdf_title = agentOutputPdf.generate_title()
    # print(pdf_title)
    print("=" * 50)
    test_point_md = generateTestPoint.agent.invoke({
        "messages": [
            {"role": "user", "content": pdf_title}
        ]
    })
    print("=" * 50)
    print(test_point_md["messages"][-1].content)
    xmind_bin = agentOutputPdf.generate_xmind()
    print(f"\n📦 已生成内存二进制，大小：{len(xmind_bin)} 字节")
    pdf_csv = agentOutputPdf.generate_csv()
    print(pdf_csv)
