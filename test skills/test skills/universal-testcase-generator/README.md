# Universal Testcase Generator

全能测试用例生成器 - 一站式测试用例生成与导出解决方案。

## 功能特点

### 多格式输入支持

- PRD文档：.docx, .md, .txt, .pdf
- 接口文档：OpenAPI/Swagger, Postman Collection, .docx, .md
- 设计截图：.png, .jpg, .gif, .webp
- 在线文档：Google Docs, Notion, Confluence, GitHub

### 多格式输出支持

- **Markdown表格**：导入测试管理系统、Excel
- **飞书思维导图**：直接粘贴到飞书思维笔记
- **XMind格式**：导入XMind思维导图工具

### 测试类型覆盖

- 功能测试用例
- 接口测试用例
- 性能测试用例
- 自动化测试用例
- UI测试用例

---

## 快速开始
在main.py启动即可启动服务器
### 根据文档生成测试用例

```
请根据这份PRD生成测试用例，导出飞书格式
[上传 PRD.docx]
```

### 根据接口文档生成

```
根据这个Swagger文档生成接口测试用例
[上传 swagger.json]
```

### 格式转换

```
把这个测试用例转成飞书思维导图格式
[粘贴测试用例]
```

---

## 输出格式选择

### Markdown 表格

**适用场景**：
- 导入测试管理系统（Jira、禅道、TestLink）
- 需要Excel格式导出
- 团队使用表格形式管理用例

### 飞书思维导图格式

**适用场景**：
- 团队使用飞书协作
- 需要思维导图可视化
- 便于快速浏览用例结构

**格式要求**：
- 纯列表结构（所有行以 `-` 开头）
- 2空格缩进
- 不使用 `##` 标题

### XMind 格式

**适用场景**：
- 团队使用 XMind 工具
- 需要专业的思维导图展示
- 需要导出图片/PDF

---

## 目录结构

```
universal-testcase-generator/
├── SKILL.md                              # 技能主文件
├── README.md                             # 使用说明
├── references/                           # 参考标准文档
│   ├── functional-testcases-standard.md  # 功能测试标准
│   ├── api-testcases-standard.md         # 接口测试标准
│   ├── performance-testcases-standard.md # 性能测试标准
│   ├── automation-testcases-standard.md  # 自动化测试标准
│   ├── xmind-format-guide.md             # XMind格式指南
│   └── feishu-format-guide.md            # 飞书格式指南
├── scripts/                              # 导出脚本
│   ├── export_to_feishu.py
│   ├── export_to_xmind.py
│   └── convert_format.py
└── assets/                               # 资源目录
```

---

## 优先级说明

| 优先级 | 定义 | 占比 |
|-------|------|------|
| P0 | 核心功能、主流程 | 10-15% |
| P1 | 重要功能、主流场景 | 25-30% |
| P2 | 一般功能、辅助流程 | 35-40% |
| P3 | 边缘功能、特殊场景 | 15-20% |

---

## 安装位置

- **用户技能**: `~/.workbuddy/skills/universal-testcase-generator/`
- **项目技能**: `.workbuddy/skills/universal-testcase-generator/`

用户技能在所有项目中可用，项目技能仅在当前项目可用。

---

## 版本信息

- **版本**: 1.0.0
- **整合来源**: doc-based-testcase-generator + prd-to-xmind-testcases
- **创建日期**: 2026-04-02
