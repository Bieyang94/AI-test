
import re
import csv
import logging
from io import StringIO

from app.core.plan.reactor import ReactAgent

logger = logging.getLogger(__name__)

_agent: ReactAgent | None = None


def _get_agent() -> ReactAgent:
    global _agent
    if _agent is None:
        _agent = ReactAgent()
    return _agent


_HEADER_KEYWORDS = ["标题", "前置条件", "步骤描述", "预期结果"]


def _find_csv_header(text: str) -> re.Match | None:
    pattern_comma = r"标题\s*,\s*前置条件\s*,\s*步骤描述\s*,\s*预期结果[\s\S]*"
    match = re.search(pattern_comma, text)
    if match:
        return match

    pattern_pipe = r"\|\s*标题\s*\|\s*前置条件\s*\|\s*步骤描述\s*\|\s*预期结果\s*\|[\s\S]*"
    return re.search(pattern_pipe, text)


def _normalize_pipe_table(table_text: str) -> str:
    lines = table_text.strip().splitlines()
    csv_lines = []
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("|"):
            stripped = stripped.strip("|")
        if re.match(r"^[\s\-:|]+$", stripped):
            continue
        cells = [cell.strip() for cell in stripped.split("|")]
        csv_lines.append(cells)

    output = StringIO()
    writer = csv.writer(output)
    for row in csv_lines:
        writer.writerow(row)
    return output.getvalue()


def generate_testcase_csv(message: str) -> str | None:
    agent = _get_agent()

    full_response = ""
    for chunk in agent.execute_stream(message):
        full_response += str(chunk)

    csv_text = full_response.strip()
    logger.info("AI 原始响应长度=%d, 前200字符: %s", len(csv_text), csv_text[:200])

    if not csv_text:
        logger.error("AI 响应为空，CSV 生成失败")
        return None

    match = _find_csv_header(csv_text)
    if not match:
        logger.error("未匹配到 CSV 表头，AI 响应不含 [%s]", ",".join(_HEADER_KEYWORDS))
        logger.debug("AI 完整响应:\n%s", csv_text)
        return None

    table_content = match.group(0).strip()

    if table_content.lstrip().startswith("|"):
        return _normalize_pipe_table(table_content)

    output = StringIO()
    writer = csv.writer(output)
    for line in table_content.splitlines():
        row = next(csv.reader([line]))
        writer.writerow(row)

    csv_str = output.getvalue()
    logger.info("CSV 生成成功，行数约=%d", csv_str.count("\n"))
    return csv_str
