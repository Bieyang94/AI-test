# AI-test Frontend

AI 测试平台前端系统，面向测试人员，可基于 PRD 文档提取功能大纲、生成思维导图（XMind）和测试用例（CSV）。

## 技术栈

- **框架**: Vue 3 + TypeScript
- **构建工具**: Vite 8
- **路由**: Vue Router 5
- **HTTP 客户端**: Axios + Fetch API（SSE 流式响应 & 二进制文件下载）
- **测试**: Vitest + Vue Test Utils
- **代码格式化**: oxfmt

## 环境要求

- Node.js `^20.19.0 || >=22.12.0`

## 快速开始

安装依赖
npm install
启动开发服务器
npm run dev
构建生产包（含类型检查）
npm run build
预览构建结果
npm run preview
运行单元测试
npm run test:unit
格式化代码
npm run format

## 项目结构

```
src/
├── api/ # API 接口封装
├── assets/ # 静态资源
├── components/ # 组件
│ ├── chat/ # 聊天相关组件（输入框、操作面板、大纲面板）
│ ├── common/ # 通用组件（加载动画、步骤指示器）
│ └── layout/ # 布局组件（侧边栏）
├── composables/ # 组合式函数
├── router/ # 路由配置
├── utils/ # 工具函数
├── views/ # 页面视图
├── App.vue # 根组件
└── main.ts # 入口文件
```

## 核心功能

1. **PRD 文件上传** — 上传产品需求文档
2. **大纲生成** — 基于 PRD 通过 SSE 流式输出提取功能大纲
3. **XMind 生成** — 将大纲转换为思维导图文件并下载
4. **CSV 生成** — 将大纲转换为测试用例表格并下载

## 环境配置

| 变量 | 说明 | 默认值 |
| --- | --- | --- |
| `VITE_APP_TITLE` | 应用标题 | `CheryGPT` |
| `VITE_API_BASE_URL` | API 基础路径 | `/file` |


