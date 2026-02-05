from __future__ import annotations

from typing import Any, Dict, List, Literal, Optional

from pydantic import BaseModel, Field


EntityLevel = Literal["global", "structure", "semantic"]


class ExtractionRequest(BaseModel):
    doc_id: str
    title: Optional[str] = None
    text: str
    metadata: Dict[str, Any] = Field(default_factory=dict)


class ExtractedEntity(BaseModel):
    id: str
    name: str
    entity_type: str
    level: EntityLevel
    confidence: float = 0.0
    evidence: List[str] = Field(default_factory=list)
    attributes: Dict[str, Any] = Field(default_factory=dict)


class ExtractedRelation(BaseModel):
    id: str
    head_id: str
    relation_type: str
    tail_id: str
    confidence: float = 0.0
    evidence: List[str] = Field(default_factory=list)


class AgentOutput(BaseModel):
    agent_name: str
    level: Literal["global", "structure", "semantic", "relation"]
    entities: List[ExtractedEntity] = Field(default_factory=list)
    relations: List[ExtractedRelation] = Field(default_factory=list)
    raw_response: Dict[str, Any] = Field(default_factory=dict)


class PipelineOutput(BaseModel):
    doc_id: str
    title: Optional[str] = None
    entities: List[ExtractedEntity]
    relations: List[ExtractedRelation]
    agent_outputs: List[AgentOutput]
