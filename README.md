# AI-Test Service

> 面向测试人员的 AI Agent 服务，基于 PRD（产品需求文档）自动提取功能大纲、生成思维导图（XMind）和测试用例（CSV）。

## ✨ 功能特性

- **文件上传**：支持 `.md` / `.docx` / `.pdf` 格式的 PRD 文档上传
- **大纲生成**：基于 LLM Agent 流式输出（SSE）功能需求大纲
- **思维导图生成**：将大纲自动转换为 XMind 思维导图文件
- **测试用例生成**：基于功能点自动生成 CSV 格式测试用例
- **内存缓存机制**：文件与生成结果均在内存中缓存，支持 TTL 自动过期
- **流式输出**：大纲生成支持 SSE 流式返回，实时展示生成进度

## 🛠️ 技术栈

| 类别 | 技术 |
|------|------|
| Web 框架 | FastAPI + Uvicorn |
| AI / Agent | LangChain + LangGraph + DeepAgents |
| LLM 调用 | DashScope（通义千问） |
| 前端 | Streamlit |
| 文档解析 | PyMuPDF / pdfplumber / python-docx / docx2txt |
| 数据导出 | openpyxl / pandas / xmind |
| 包管理 | uv + pyproject.toml |

## 📋 环境要求

- Python >= 3.12
- [uv](https://docs.astral.sh/uv/) 包管理器（推荐）

## 🚀 快速开始

### 1. 克隆项目

git clone
cd AI-test

### 2. 安装依赖

uv sync

### 3. 配置环境变量

在项目根目录创建 `.env` 文件：
env API_KEY=your-dashscope-api-key
APP_NAME=AI-Test Service APP_VERSION=1.0.0 DEBUG=false
HOST=your-host PORT=your-port LOG_LEVEL=INFO
CACHE_MAX_ENTRIES=100 CACHE_TTL_SECONDS=3600
MAX_UPLOAD_SIZE_MB=30 CORS_ORIGINS=["*"]

### 4. 启动服务

uv run python -m app.service.server.main

服务启动后访问：
- 接口地址：`your-host:your-port/file`
- API 文档（DEBUG 模式下）：`http://127.0.0.1:8000/docs`

## 📡 API 接口

所有接口均以 `/file` 为前缀，完整调用链路如下：
上传文件 → 生成大纲 → 生成 XMind → 生成 CSV

| 方法 | 路径 | 说明 |
|------|------|------|
| `POST` | `/file/upload` | 上传 PRD 文件（md/docx/pdf），返回缓存编号 `num` |
| `POST` | `/file/generateOutline?num={num}` | 基于上传文件流式生成大纲（SSE） |
| `POST` | `/file/generateXmind?num={num}` | 基于大纲生成 XMind 文件下载 |
| `POST` | `/file/getXmindTestPoints?num={num}` | 获取 XMind 中提取的功能点文本 |
| `POST` | `/file/generateCsv?num={num}` | 基于功能点生成 CSV 测试用例下载 |
| `POST` | `/file/getCsv?num={num}` | 获取已缓存的 CSV 文件 |
| `DELETE` | `/file/cache/{num}` | 清除指定编号的所有缓存 |
| `GET` | `/` | 服务信息 |
| `GET` | `/health` | 健康检查 |

### 典型调用流程

1. 上传 PRD 文件，获取编号
curl -X POST http://127.0.0.1:8000/file/upload -F "file=@prd.docx"
→ {"num": 1, "ext": "docx", ...}
2. 生成大纲（SSE 流式）
curl -X POST "http://127.0.0.1:8000/file/generateOutline?num=1"
3. 生成 XMind 思维导图
curl -X POST "http://127.0.0.1:8000/file/generateXmind?num=1" -o outline.xmind
4. 生成 CSV 测试用例
curl -X POST "http://127.0.0.1:8000/file/generateCsv?num=1" -o testcase.csv

## 📁 项目结构
```
AI-test/ 
├── app/ 
│ ├── core/ # 核心业务逻辑 
│ │ ├── Frontend/ # Streamlit 前端 
│ │ │ └── chat.py 
│ │ ├── data_transformer/ # 数据格式转换 
│ │ │ ├── generate_stream_xmind.py 
│ │ │ ├── markdown_to_csv.py 
│ │ │ └── markdown_to_xlsx.py 
│ │ ├── interface/ # Agent 输出接口 
│ │ │ └── agent_output.py 
│ │ ├── model/ # LLM 模型封装 
│ │ │ └── llm.py 
│ │ ├── plan/ # Agent 规划与提示词 
│ │ │ ├── architecture.py 
│ │ │ ├── class_state.py 
│ │ │ ├── function_requiremen.py 
│ │ │ ├── reactor.py 
│ │ │ ├── sys_prompt.py 
│ │ │ └── ... 
│ │ └── tools/ # 文档解析工具 
│ │ ├── extract_mdToheader.py 
│ │ ├── extract_pdf.py 
│ │ └── extract_word.py 
│ └── service/ # 服务层 
│ └── server/ 
│ ├── cache/ # 内存缓存（文件/大纲/XMind/CSV） 
│ ├── router/ # FastAPI 路由 
│ │ ├── upload.py 
│ │ ├── generate_outline_stream.py 
│ │ ├── generate_xmind_stream.py 
│ │ └── generate_csv.py 
│ ├── config.py # 配置管理 
│ ├── logging_config.py # 日志配置 
│ └── main.py # 应用入口 
├── .env # 环境变量 
├── pyproject.toml # 项目依赖 
└── uv.lock # 依赖锁文件
```
## 📄 License

Public

这份 README 涵盖了以下内容：
项目简介 — 一句话说明项目定位和核心能力
功能特性 — 列出所有关键功能
技术栈 — 表格形式清晰展示
环境要求 & 快速开始 — 从克隆到启动的完整步骤
API 接口文档 — 所有接口的路径、方法、说明，附带典型调用流程示例
项目结构 — 带注释的目录树
环境变量配置 — 完整的 .env 示例