import pandas as pd


data = {
    "序号": [1, 2, 3, 4, 5],
    "标题": ["测试数据1", "测试数据2", "测试数据3", "测试数据4", "测试数据5"],
    "内容描述": ["内容A", "内容B", "内容C", "内容D", "内容E"],
}

# 转为DataFrame表格
df = pd.DataFrame(data)

# ====================== 导出 .xlsx Excel 文件 ======================
df.to_excel("data.xlsx", index=False, engine="openpyxl")