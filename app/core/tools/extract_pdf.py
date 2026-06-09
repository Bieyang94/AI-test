import fitz  # PyMuPDF
import pdfplumber
import pandas as pd
from io import BytesIO, StringIO

from app.core.plan import reactor

# ======================
# 核心 PDF 解析类（全内存，支持路径 / 二进制）
# ======================
class PDFMemoryParser:
    def __init__(self, pdf_source: str | bytes | BytesIO):
        """
        初始化：支持 3 种输入
        - str: 本地 PDF 文件路径
        - bytes: PDF 二进制字节流
        - BytesIO: PDF 内存流
        所有数据均存储在内存中，不写入本地
        """
        self.pdf_source = pdf_source
        self.all_text = ""  # 合并后的全文本
        self.images = []   # 图片列表：[{"page": 页码, "index": 序号, "bytes": 字节流, "ext": 后缀}]
        self.tables = []   # 表格列表：[{"page": 页码, "index": 序号, "csv_text": CSV文本, "data": 原始数据}]

    def parse(self):
        """统一执行解析：文本 + 图片 + 表格"""
        self._extract_images()
        self._extract_text_and_tables()
        return self

    def _get_pdf_stream(self) -> BytesIO:
        """内部工具：统一将输入转为 BytesIO 流"""
        if isinstance(self.pdf_source, str):
            # 路径：读取为二进制流
            with open(self.pdf_source, "rb") as f:
                return BytesIO(f.read())
        elif isinstance(self.pdf_source, bytes):
            # 二进制：直接包装
            return BytesIO(self.pdf_source)
        elif isinstance(self.pdf_source, BytesIO):
            # 已经是流：直接返回
            return self.pdf_source
        else:
            raise TypeError("仅支持路径(str)、二进制(bytes)、BytesIO")

    def _extract_images(self):
        """提取图片到内存（PyMuPDF，支持二进制）"""
        stream = self._get_pdf_stream()
        doc = fitz.open("pdf", stream)  # 直接从内存流打开
        for page_idx, page in enumerate(doc):
            page_num = page_idx + 1
            imgs = page.get_images(full=True)
            for img_idx, xref in enumerate(imgs):
                img_info = doc.extract_image(xref[0])
                self.images.append({
                    "page": page_num,
                    "index": img_idx + 1,
                    "bytes": img_info["image"],
                    "ext": img_info["ext"]
                })
        doc.close()

    def _extract_text_and_tables(self):
        """提取文本（合并）+ 表格（CSV内存文本，支持二进制）"""
        stream = self._get_pdf_stream()
        with pdfplumber.open(stream) as pdf:  # 直接从内存流打开
            for page_idx, page in enumerate(pdf.pages):
                page_num = page_idx + 1

                # 提取文本
                text = page.extract_text()
                if text and text.strip():
                    self.all_text += text.strip() + "\n\n"

                # 提取表格
                tables = page.extract_tables()
                for tb_idx, table in enumerate(tables):
                    if not table or all(not row for row in table):
                        continue

                    df = pd.DataFrame(table)
                    csv_buffer = StringIO()
                    df.to_csv(csv_buffer, index=False, header=False, encoding="utf-8")
                    csv_text = csv_buffer.getvalue()

                    self.tables.append({
                        "page": page_num,
                        "index": tb_idx + 1,
                        "csv_text": csv_text,
                        "raw_data": table
                    })

# ======================
# 对外调用接口（兼容路径 / 二进制）
# ======================
def parse_pdf_to_memory(pdf_source: str | bytes | BytesIO) -> dict:
    """
    最简洁的调用接口
    支持：文件路径 / PDF二进制 / BytesIO
    返回：全文本、图片列表、表格CSV列表
    """
    parser = PDFMemoryParser(pdf_source).parse()
    return {
        "full_text": parser.all_text,
        "images": parser.images,
        "tables": parser.tables
    }


def extract_text_only(pdf_source: str | bytes | BytesIO) -> str:
    """仅提取 PDF 文本，不调用 LLM"""
    return parse_pdf_to_memory(pdf_source)["full_text"]


def generate_title_by_model(pdf_source: str | bytes | BytesIO):
    """支持路径 / 二进制 生成标题"""
    full_text = parse_pdf_to_memory(pdf_source)["full_text"]
    extractor_title_agent = reactor.extract_title_ReactorAgent()
    requirement_pdf =extractor_title_agent.execute_stream(full_text)
    return requirement_pdf


def generate_csv_by_model(pdf_source: str | bytes | BytesIO):
    """支持 路径 / 二进制 生成CSV内容"""
    full_text = parse_pdf_to_memory(pdf_source)["full_text"]
    test_csv_agent = reactor.ReactAgent()
    result = test_csv_agent.agent.invoke({
        "messages": [
            {"role": "user", "content": full_text}
        ]
    })
    return result["messages"][-1].content


# ======================
# 使用示例（路径 / 二进制 都可以）
# ======================
if __name__ == "__main__":
    pdf_file = r"C:\Users\EDY\Desktop\掘金2.0产品需求文档 .pdf"

    # ============= 方式1：传入路径（原有用法） =============
    # result = parse_pdf_to_memory(pdf_file)
    # title = generate_title_by_model(pdf_file)
    # csv = generate_csv_by_model(pdf_file)

    # ============= 方式2：传入二进制字节流（新增） =============
    with open(pdf_file, "rb") as f:
        pdf_bytes = f.read()  # 拿到 PDF 二进制

    # 直接用 bytes 解析
    # result = parse_pdf_to_memory(pdf_bytes)
    title = generate_title_by_model(pdf_bytes)
    # csv_content = generate_csv_by_model(pdf_bytes)

    # print("标题：", title)
    # print("CSV：", csv_content)