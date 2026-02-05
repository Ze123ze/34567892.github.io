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
- 对齐本体中的核心类、数据属性、对象属性约束
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
  config.py           # 本体类、实体类型、关系约束配置
  llm_client.py       # OpenAI 兼容 API 客户端
  models.py           # 数据模型
  pipeline.py         # 流水线编排
  main.py             # CLI 入口
```

## 5. 本体对齐说明

当前代码已对齐你定义的核心本体结构：

- 13 个核心类：Policy、Provision、PolicyTool、EligibilityCondition、PolicyTarget、Project、PolicyBackground、PolicyInitiative、PolicyObjective、DomainTheme、Organization、Jurisdiction、TimePeriod。
- Provision 作为独立类，不再是 Policy 的普通属性。
- 抽取时 `attributes` 字段承载对应类的数据属性（例如 Policy 的 `policyId/documentNumber/effectiveDate` 等）。
- 关系抽取使用标准对象属性（例如 `hasProvision`、`supportsProject`、`sourceProvision`、`hasJurisdictionOver` 等）并做方向性约束校验。

