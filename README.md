# 深海科技政策知识图谱（Multi-Agent Pipeline）

这是一个可直接部署的**多智能体流水线**项目骨架，用于从政策文本中抽取实体与关系，并输出知识图谱结构化结果。

## 1. 项目目标

围绕你定义的 13 类实体，按三层抽取：

- 全局层（文档级）：政策、机构、管辖区域、时间区间、领域主题
- 结构层（条文级）：政策条文、项目、政策对象、适用条件
- 语义层（内容级）：政策背景、政策目标、政策举措、政策工具
- 关系层：跨层关系抽取（独立关系智能体）

## 2. 功能概览

- 支持 OpenAI 兼容的大模型 API（可替换为任意兼容 endpoint）
- 4 组智能体协作：Global / Structure / Semantic / Relation
- 分层输出、统一标准化、可追溯 evidence
- FastAPI 服务化部署，提供 HTTP 接口

## 3. 快速开始

### 3.1 安装依赖

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 3.2 配置环境变量

```bash
cp .env.example .env
```

按需修改：

- `LLM_BASE_URL`
- `LLM_API_KEY`
- `LLM_MODEL`

### 3.3 启动 API 服务

```bash
uvicorn policy_kg_pipeline.api_server:app --host 0.0.0.0 --port 8000 --reload
```

### 3.4 调用示例

```bash
curl -X POST http://localhost:8000/v1/pipeline/extract \
  -H "Content-Type: application/json" \
  -d '{
    "doc_id": "policy-001",
    "title": "某深海科技专项政策",
    "text": "（在此粘贴完整政策文本）",
    "metadata": {"source": "示例"}
  }'
```

## 4. 目录结构

```text
policy_kg_pipeline/
  api_server.py       # FastAPI 入口
  agents.py           # 各层智能体定义
  config.py           # 实体类型与层级配置
  llm_client.py       # OpenAI 兼容 API 客户端
  models.py           # 数据模型
  pipeline.py         # 流水线编排
  main.py             # CLI 入口
```

## 5. 后续你需要补充的内容

你提到“实体英文名与关系类型后续提供”，本项目已预留：

- `config.py > ENTITY_TYPES`：补充 `english_name`
- `config.py > RELATION_TYPES`：补充关系标签、头尾实体约束
- `agents.py` 中的 prompts：可按领域术语进一步强化

