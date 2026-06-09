import re
import json
import logging
import xmind
from xmind.core.topic import TopicElement
from typing import Dict, List, Optional, Union
from pathlib import Path
import tempfile

from app.core.plan import reactor

logger = logging.getLogger(__name__)


def generate_requirement_by_model(content: str) -> str:
    requirement_agent = reactor.extract_title_ReactorAgent()
    requirement_md = requirement_agent.execute_stream(content)
    return requirement_md


def _strip_code_fences(content: str) -> str:
    content = re.sub(r"^\s*$", "", content, flags=re.MULTILINE)
    return content.strip()


def extract_markdown_headers(content: str) -> List[Dict[str, Union[int, str]]]:
    if not isinstance(content, str) or not content.strip():
        return []
    content = _strip_code_fences(content)
    pattern = r'^(#{1,6})\s+(.+?)$'
    matches = re.findall(pattern, content, re.MULTILINE)
    return [{"level": len(h), "text": t.strip()} for h, t in matches]


def _extract_list_items(content: str) -> List[Dict[str, Union[int, str]]]:
    content = _strip_code_fences(content)
    items = []
    for line in content.splitlines():
        stripped = line.strip()
        if not stripped:
            continue

        bold_match = re.match(r"^(#{0})\*\*(.+?)\*\*\s*$", stripped)

        indent_match = re.match(r"^(\s*)[-*]\s+(.+)$", stripped)
        if indent_match:
            indent_len = len(indent_match.group(1))
            text = indent_match.group(2).strip()
            text = re.sub(r"\*\*(.+?)\*\*", r"\1", text)
            level = min(indent_len // 2 + 2, 6)
            if text:
                items.append({"level": level, "text": text})
            continue

        num_match = re.match(r"^(\s*)(\d+)[.)]\s+(.+)$", stripped)
        if num_match:
            indent_len = len(num_match.group(1))
            text = num_match.group(3).strip()
            text = re.sub(r"\*\*(.+?)\*\*", r"\1", text)
            level = min(indent_len // 2 + 2, 6)
            if text:
                items.append({"level": level, "text": text})
            continue

        if bold_match:
            text = bold_match.group(1).strip()
            if text:
                items.append({"level": 1, "text": text})

    return items


def build_header_tree(headers: List[Dict[str, Union[int, str]]]) -> List[Dict]:
    if not isinstance(headers, list):
        return []

    root = []
    stack = []
    for header in headers:
        try:
            level = int(header.get("level", 0))
            text = str(header.get("text", "")).strip()
            if level < 1 or level > 6 or not text:
                continue

            node = {"title": text, "level": level, "children": []}
            while stack and stack[-1]["level"] >= level:
                stack.pop()

            if not stack:
                root.append(node)
            else:
                stack[-1]["children"].append(node)
            stack.append(node)
        except (ValueError, TypeError):
            continue
    return root


def markdown_to_tree_json(content: str, indent: int = 2) -> str:
    headers = extract_markdown_headers(content)
    if not headers:
        logger.info("未找到 # 标题，尝试列表项回退解析")
        headers = _extract_list_items(content)
    tree = build_header_tree(headers)
    return json.dumps(tree, ensure_ascii=False, indent=indent)


# ====================== 纯净版：只返回内存二进制，不生成本地文件 ======================
def generate_xmind(
        content: Optional[str] = None,
        md_file_path: Optional[Union[str, Path]] = None,
        sheet_title: str = "思维导图",
) -> Dict[str, Optional[Union[str, bytes]]]:
    result = {
        "xmind_bytes": None,
        "error": None
    }

    try:
        md_content = ""
        if content and content.strip():
            md_content = content.strip()
        elif md_file_path:
            with open(md_file_path, "r", encoding="utf-8") as f:
                md_content = f.read().strip()
        else:
            raise ValueError("必须传入 content 或 md_file_path")

        if not md_content:
            raise ValueError("Markdown 内容为空")

        tree_data = json.loads(markdown_to_tree_json(md_content))
        if not tree_data:
            logger.error("解析失败，内容前300字符: %s", md_content[:300])
            raise ValueError("未提取到任何标题或列表结构")

        with tempfile.NamedTemporaryFile(suffix=".xmind", delete=False) as tmp:
            tmp_path = tmp.name
        workbook = xmind.load(tmp_path)
        Path(tmp_path).unlink(missing_ok=True)

        sheet = workbook.getPrimarySheet()
        sheet.setTitle(sheet_title)
        root_topic = sheet.getRootTopic()
        root_topic.setTitle("思维导图")

        def add_children(parent: TopicElement, nodes: List[Dict]):
            for node in nodes:
                sub = parent.addSubTopic()
                sub.setTitle(node["title"])
                add_children(sub, node.get("children", []))

        add_children(root_topic, tree_data)

        with tempfile.NamedTemporaryFile(suffix=".xmind", delete=False) as temp_file:
            temp_xmind_path = temp_file.name

        xmind.save(workbook, temp_xmind_path)

        with open(temp_xmind_path, "rb") as f:
            result["xmind_bytes"] = f.read()

        Path(temp_xmind_path).unlink(missing_ok=True)

        logger.info("XMind 内存二进制生成成功，大小=%d bytes", len(result["xmind_bytes"]))

    except Exception as e:
        result["error"] = f"生成失败：{str(e)}"
        logger.error("XMind 生成失败: %s", e)

    return result


def markdown_to_xmind(content: str, **kwargs) -> Dict[str, Optional[Union[str, bytes]]]:
    return generate_xmind(content=content, **kwargs)


def generate_csv_by_model(md_source: str):
    full_text = md_source
    test_csv_agent = reactor.ReactAgent()
    result = test_csv_agent.agent.invoke({
        "messages": [
            {"role": "user", "content": full_text}
        ]
    })
    return result["messages"][-1].content

