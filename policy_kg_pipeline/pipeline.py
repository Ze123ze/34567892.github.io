from __future__ import annotations

from typing import List

from .agents import EntityLayerAgent, RelationAgent
from .llm_client import LLMClient
from .models import AgentOutput, PipelineOutput


class MultiAgentKGPipeline:
    def __init__(self, llm_client: LLMClient | None = None) -> None:
        client = llm_client or LLMClient()
        self.global_agent = EntityLayerAgent("global-agent", "global", client)
        self.structure_agent = EntityLayerAgent("structure-agent", "structure", client)
        self.semantic_agent = EntityLayerAgent("semantic-agent", "semantic", client)
        self.relation_agent = RelationAgent("relation-agent", "relation", client)

    async def run(self, doc_id: str, title: str | None, text: str) -> PipelineOutput:
        outputs: List[AgentOutput] = []

        global_out = await self.global_agent.run(doc_id, title, text, context={})
        outputs.append(global_out)

        structure_out = await self.structure_agent.run(doc_id, title, text, context={})
        outputs.append(structure_out)

        semantic_out = await self.semantic_agent.run(doc_id, title, text, context={})
        outputs.append(semantic_out)

        entities = global_out.entities + structure_out.entities + semantic_out.entities

        relation_out = await self.relation_agent.run(
            doc_id,
            title,
            text,
            context={"entities": [e.model_dump() for e in entities]},
        )
        outputs.append(relation_out)

        return PipelineOutput(
            doc_id=doc_id,
            title=title,
            entities=entities,
            relations=relation_out.relations,
            agent_outputs=outputs,
        )
