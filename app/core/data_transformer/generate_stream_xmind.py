import xmind
from xmind.core.topic import TopicElement
import io
import zipfile
import json

# 1. 生成器：递归产出节点（边遍历边产出）
def generate_topics(root: TopicElement):
    yield {"title": root.getTitle(), "id": root.getId()}
    for child in root.getSubTopics():
        yield from generate_topics(child)

# 2. 流式构建 XMind 并写入内存流
def build_xmind_stream():
    # 创建工作簿（内存中）
    workbook = xmind.load()  # 不指定路径，纯内存
    sheet = workbook.getPrimarySheet()
    root = sheet.getRootTopic()
    root.setTitle("流式输出根节点")

    # 模拟：逐步添加子节点（可替换为你的业务数据）
    for i in range(1, 4):
        level1 = root.addSubTopic()
        level1.setTitle(f"一级节点 {i}")
        for j in range(1, 3):
            level2 = level1.addSubTopic()
            level2.setTitle(f"二级节点 {i}-{j}")

    # 写入内存 BytesIO（ZIP 格式）
    bio = io.BytesIO()
    workbook.save(bio)  # 直接写流，不落地
    bio.seek(0)  # 重置指针到开头
    return bio, generate_topics(root)

# 3. 测试：获取流 + 迭代节点
if __name__ == "__main__":
    xmind_stream, topic_generator = build_xmind_stream()
    # 流式打印节点（边生成边输出）
    for node in topic_generator:
        print("产出节点:", node)
    # 保存到本地验证（可选）
    with open("streamed.xmind", "wb") as f:
        f.write(xmind_stream.getvalue())