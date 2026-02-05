from __future__ import annotations

import uuid
from typing import Any, Dict, List

from .config import ENTITY_TYPES, LEVEL_TO_ENTITY_TYPES, RELATION_CONSTRAINTS, RELATION_TYPES
from .llm_client import LLMClient, build_context_block, compact_entities_for_prompt
from .models import AgentOutput, ExtractedEntity, ExtractedRelation


class BaseAgent:
    def __init__(self, agent_name: str, level: str, llm_client: LLMClient) -> None:
        self.agent_name = agent_name
        self.level = level
        self.llm_client = llm_client

    async def run(self, doc_id: str, title: str | None, text: str, context: Dict[str, Any]) -> AgentOutput:
        raise NotImplementedError

    @staticmethod
    def _to_entities(items: List[Dict[str, Any]], level: str) -> List[ExtractedEntity]:
        result: List[ExtractedEntity] = []
        for item in items:
            result.append(
                ExtractedEntity(
                    id=item.get("id") or f"ent-{uuid.uuid4().hex[:10]}",
                    name=item.get("name", ""),
                    entity_type=item.get("entity_type", ""),
                    ontology_class=item.get("ontology_class", ""),
                    level=level,
                    confidence=float(item.get("confidence", 0.0)),
                    evidence=item.get("evidence", []),
                    attributes=item.get("attributes", {}),
                )
            )
        return result

    @staticmethod
    def _to_relations(items: List[Dict[str, Any]]) -> List[ExtractedRelation]:
        result: List[ExtractedRelation] = []
        for item in items:
            result.append(
                ExtractedRelation(
                    id=item.get("id") or f"rel-{uuid.uuid4().hex[:10]}",
                    head_id=item.get("head_id", ""),
                    relation_type=item.get("relation_type", ""),
                    tail_id=item.get("tail_id", ""),
                    confidence=float(item.get("confidence", 0.0)),
                    evidence=item.get("evidence", []),
                )
            )
        return result


class EntityLayerAgent(BaseAgent):
    async def run(self, doc_id: str, title: str | None, text: str, context: Dict[str, Any]) -> AgentOutput:
        allowed_types = LEVEL_TO_ENTITY_TYPES[self.level]
        schema_hint = {
            entity_type: {
                "class": ENTITY_TYPES[entity_type].english_name,
                "required_data_properties": ENTITY_TYPES[entity_type].data_properties,
            }
            for entity_type in allowed_types
        }

        system_prompt = (
            "你是深海科技政策知识图谱抽取专家。"
            "请严格输出 JSON，字段：entities。"
            "entities 每项必须包含：id, name, entity_type, confidence, evidence, attributes。"
            f"只允许抽取以下实体类型：{allowed_types}。"
            "attributes 中仅放该实体的数据属性键值。"
            "请尽量补全本体要求的数据属性，缺失则可留空字符串。"
            "若无可抽取内容，返回空数组。"
        )
        user_prompt = f"{build_context_block(doc_id, title, text)}\n\n本体数据属性要求:\n{schema_hint}"

        raw = await self.llm_client.chat_json(system_prompt, user_prompt)
        raw_entities = raw.get("entities", [])
        filtered_entities = [e for e in raw_entities if e.get("entity_type") in allowed_types]
        for entity in filtered_entities:
            if not entity.get("ontology_class") and entity.get("entity_type") in ENTITY_TYPES:
                entity["ontology_class"] = ENTITY_TYPES[entity["entity_type"]].english_name
        entities = self._to_entities(filtered_entities, self.level)

        return AgentOutput(
            agent_name=self.agent_name,
            level=self.level,
            entities=entities,
            raw_response=raw,
        )


class RelationAgent(BaseAgent):
    async def run(self, doc_id: str, title: str | None, text: str, context: Dict[str, Any]) -> AgentOutput:
        entities = context.get("entities", [])
        id_to_type = {item["id"]: item.get("entity_type") for item in entities if item.get("id")}

        system_prompt = (
            "你是深海科技政策知识图谱关系抽取专家。"
            "请根据给定实体集合与政策文本，抽取关系。"
            "严格输出 JSON，字段：relations。"
            "relations 中每项包含：head_id, relation_type, tail_id, confidence, evidence。"
            f"relation_type 仅允许：{RELATION_TYPES}。"
            f"关系方向与类型约束：{RELATION_CONSTRAINTS}。"
            "head_id 和 tail_id 必须来自提供实体 id。"
        )
        user_prompt = (
            f"{build_context_block(doc_id, title, text)}\n\n"
            f"候选实体:\n{compact_entities_for_prompt(entities)}"
        )

        raw = await self.llm_client.chat_json(system_prompt, user_prompt)
        relations = self._to_relations(raw.get("relations", []))

        validated: List[ExtractedRelation] = []
        for rel in relations:
            if rel.relation_type not in RELATION_TYPES:
                continue
            if rel.head_id not in id_to_type or rel.tail_id not in id_to_type:
                continue
            constraints = RELATION_CONSTRAINTS.get(rel.relation_type)
            if not constraints:
                validated.append(rel)
                continue
            if id_to_type[rel.head_id] in constraints["head"] and id_to_type[rel.tail_id] in constraints["tail"]:
                validated.append(rel)

        return AgentOutput(
            agent_name=self.agent_name,
            level="relation",
            relations=validated,
            raw_response=raw,
        )
