import logging
import sys
import time
from pathlib import Path
from typing import Optional, Dict
from PyPDF2 import PdfReader
from io import BytesIO

sys.path.append(str(Path(__file__).parent.parent.parent.parent))

from app.core.interface import agent_output

import docx2txt
import streamlit as st
import streamlit.components.v1 as components
import os
import io

# 页面配置
st.set_page_config(
    page_title="AItest",
    page_icon="📄",
    layout="wide"
)
st.title("📄测试用例自动生成助手")

# ====================== Session 初始化 ======================
def init_session():
    default_state = {
        "message": [],
        "file_content": "",
        "xmind_data": None,
        "xmind_result": None,
        "csv_data": None,
        "_uploaded_file": None,
        "tools_instance": None,
        "requirement_annalyze": "",
        "need_stream": False,
        "outline_generated": False,  # 新增：标记大纲是否已生成
    }
    for key, value in default_state.items():
        if key not in st.session_state:
            st.session_state[key] = value

init_session()

# ====================== 工具函数：读取所有文件文本 ======================
def read_uploaded_file(uploaded_file) -> str:
    """统一读取文件内容：MD/DOCX/PDF 都能正常提取文本"""
    if not uploaded_file:
        return ""

    file_ext = uploaded_file.name.lower().split('.')[-1]
    file_content = ""

    try:
        # MD 文件
        if file_ext == "md":
            file_content = uploaded_file.getvalue().decode("utf-8", errors="ignore")

        # Word 文件
        elif file_ext in ["docx", "doc"]:
            file_content = docx2txt.process(uploaded_file)

        # PDF 文件
        elif file_ext == "pdf":
            pdf_reader = PdfReader(BytesIO(uploaded_file.getvalue()))
            pdf_text = []
            for page in pdf_reader.pages:
                text = page.extract_text()
                if text:
                    pdf_text.append(text)
            file_content = "\n".join(pdf_text)

        # TXT 文件
        elif file_ext == "txt":
            file_content = uploaded_file.getvalue().decode("utf-8", errors="ignore")

    except Exception as e:
        st.error(f"文件解析失败: {str(e)}")
        return ""

    return file_content

# ====================== 页面布局 ======================
col_left, col_mid, col_right = st.columns([3, 4, 3])

# 左侧：文件上传
with col_left:
    st.subheader("上传文档")
    uploaded_file = st.file_uploader(
        "支持 PDF / Markdown / word / txt 文件",
        type=["pdf", "md", "txt", "doc", "docx"]
    )

    if uploaded_file is not None:
        # 避免重复解析同一个文件
        if st.session_state["_uploaded_file"] != uploaded_file:
            st.session_state["_uploaded_file"] = uploaded_file
            st.session_state["outline_generated"] = False  # 重置大纲生成状态
            st.session_state["requirement_annalyze"] = ""
            st.session_state["tools_instance"] = None

            ext = uploaded_file.name.lower().split('.')[-1]

            # 统一：先读取内容 → 中间栏显示
            content = read_uploaded_file(uploaded_file)
            st.session_state["file_content"] = content

            try:
                # MD
                if ext == "md":
                    st.session_state["tools_instance"] = agent_output.agent_output_markdown(content)
                    st.success("MD 文件解析 & 工具初始化成功！")

                # DOCX
                elif ext in ["docx", "doc"]:
                    doc_io = BytesIO(uploaded_file.getvalue())
                    st.session_state["tools_instance"] = agent_output.agent_output_docx(doc_io)
                    st.success("DOCX 工具初始化成功！")

                # PDF
                elif ext == "pdf":
                    pdf_io = BytesIO(uploaded_file.getvalue())
                    st.session_state["tools_instance"] = agent_output.agent_output_pdf(pdf_io)
                    st.success("PDF 工具初始化成功！")

                # TXT
                elif ext == "txt":
                    st.session_state["tools_instance"] = agent_output.agent_output_markdown(content)
                    st.success("TXT 文件解析 & 工具初始化成功！")

                # 其他
                else:
                    st.warning(f"{ext.upper()} 文件已上传，暂不支持生成")

            except Exception as e:
                st.error(f"工具初始化失败: {str(e)}")

# 中间：文本内容展示 —— 【真正同步流式输出版本】
with col_mid:
    st.subheader("功能需求大纲提取")
    output_container = st.empty()

    tools_inst = st.session_state.get("tools_instance")
    outline = st.session_state.get("requirement_annalyze", "")
    outline_generated = st.session_state.get("outline_generated", False)

    # 有工具实例 + 没有生成过大纲 → 执行生成
    if tools_inst and not outline_generated:
        st.session_state["outline_generated"] = True  # 立即上锁，避免重复执行

        # 流式输出容器
        with output_container.container():
            st.markdown("##### 📝 文档大纲（生成中...）")
            stream_area = st.empty()  # 专门用来流式输出文字的区域

        full_result = ""
        # 流式输出核心逻辑
        if hasattr(tools_inst, "generate_title_stream"):
            # 逐字获取流式内容
            for chunk in tools_inst.generate_title_stream():
                full_result += chunk
                # 实时更新显示
                stream_area.markdown(full_result)
                time.sleep(0.01)  # 轻微延迟让流式效果更顺滑
        else:
            # 非流式，直接返回结果
            full_result = tools_inst.generate_title()
            stream_area.markdown(full_result)

        # 保存最终结果
        st.session_state["requirement_annalyze"] = full_result

        # 完成后刷新标题状态
        with output_container.container():
            st.markdown("##### 📝 文档大纲 ✅")
            st.markdown(full_result)

    # 已经生成过大纲 → 直接展示
    elif outline:
        with output_container.container():
            st.markdown("##### 📝 文档大纲 ✅")
            st.markdown(outline)

# 右侧：操作区
with col_right:
    st.subheader("思维导图 & 测试用例")
    tools_instance = st.session_state.get("tools_instance")
    doc_content = st.session_state.get("file_content", "")

    # 1. 生成思维导图
    if st.button("生成思维导图"):
        if not doc_content or not tools_instance:
            st.error("请先在左侧上传文档！")
        else:
            with st.spinner("正在生成思维导图..."):
                try:
                    xmind_data = tools_instance.generate_xmind()
                    if isinstance(xmind_data, str):
                        xmind_data = xmind_data.encode('utf-8')
                    st.session_state["xmind_data"] = xmind_data
                    st.success("思维导图生成完成！")
                except Exception as e:
                    st.error(f"生成失败: {str(e)}")

    if st.session_state.get("xmind_data") is not None:
        st.download_button(
            label="📥 下载 XMind 思维导图",
            data=st.session_state["xmind_data"],
            file_name="测试用例思维导图.xmind",
            mime="application/xmind",
            use_container_width=True
        )

    st.divider()

    # 2. 生成测试用例CSV
    st.subheader("测试用例结果")
    if st.button("生成测试用例 CSV"):
        if not doc_content or not tools_instance:
            st.error("请先上传文档！")
        else:
            with st.spinner("正在生成测试用例..."):
                try:
                    csv_data = tools_instance.generate_csv()
                    if isinstance(csv_data, str):
                        csv_data = csv_data.encode('utf-8-sig')
                    st.session_state["csv_data"] = csv_data
                    st.success("测试用例 CSV 生成成功！")
                except Exception as e:
                    st.error(f"生成CSV失败: {str(e)}")

    if st.session_state.get("csv_data") is not None:
        st.download_button(
            label="📥 下载测试用例 CSV",
            data=st.session_state["csv_data"],
            file_name="测试用例.csv",
            mime="text/csv",
            use_container_width=True
        )