# 企业情报分析 Agent 工作流平台

一个面向竞品分析与行业研究场景的 AI Agent 工作流系统。  
系统支持任务解析、执行规划、Web 信息检索、本地知识库检索、分析摘要生成、Markdown 报告导出、任务历史管理与知识库上传扩展。

## 1. 项目背景

在企业情报分析、竞品研究和行业观察场景中，传统流程通常需要人工完成：
- 明确分析任务
- 搜集外部资料
- 查阅内部资料
- 归纳关键动态
- 生成分析报告

该项目基于大模型应用工程思路，构建了一个可演示、可扩展的 Agent 工作流平台，用于自动完成上述流程。

## 2. 核心功能

### 2.1 任务解析
用户输入自然语言任务，例如：
- 分析过去7天 Perplexity 和 Kimi 的产品动态，输出竞品日报
- 分析过去30天 AI 搜索赛道的发展动态，输出行业观察报告

系统会自动解析：
- 任务类型
- 目标公司
- 时间范围
- 输出格式
- 是否需要竞品对比

### 2.2 执行规划
系统会根据解析结果自动生成执行计划，例如：
- collect_web_data
- collect_kb_data
- extract_key_updates
- compare_competitors
- generate_report

### 2.3 Web 信息检索
当前版本支持 mock / real 模式切换，完成外部信息获取能力抽象，便于后续替换为真实搜索服务。

### 2.4 本地知识库检索
支持基于本地知识库文件进行轻量检索。  
同时支持上传 txt / md / pdf 文件并动态追加到知识库。

### 2.5 分析与报告生成
系统可自动输出：
- 分析摘要
- 关键动态
- 竞品对比表
- Markdown 报告

### 2.6 历史任务管理
系统支持：
- 任务历史保存
- 历史任务查看
- 单条删除
- 全部清空

## 3. 技术架构

### 后端
- FastAPI
- SQLite
- Pydantic

### 前端
- Streamlit

### Agent / Workflow
- 规则式任务解析
- 规则式执行规划
- 统一任务执行器

### 知识库
- 本地文本知识库
- PDF/TXT/MD 文件导入
- 轻量检索器

## 4. 项目结构

```bash
intel_agent_platform/
├── app/
│   ├── api/
│   ├── schemas/
│   └── main.py
├── agent/
│   ├── planner.py
│   └── executor.py
├── tools/
│   ├── web_search.py
│   ├── kb_search.py
│   ├── analyzer.py
│   └── report_generator.py
├── rag/
│   ├── retriever.py
│   └── ingestion.py
├── utils/
│   ├── config.py
│   └── db.py
├── frontend/
│   └── streamlit_app.py
├── data/
│   ├── raw/
│   └── reports/
├── db/
│   └── app.db
└── README.md