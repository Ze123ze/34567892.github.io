from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List


@dataclass(frozen=True)
class EntityType:
    chinese_name: str
    english_name: str
    level: str


ENTITY_TYPES: Dict[str, EntityType] = {
    "政策": EntityType("政策", "policy", "global"),
    "政策条文": EntityType("政策条文", "policy_clause", "structure"),
    "政策工具": EntityType("政策工具", "policy_instrument", "semantic"),
    "适用条件": EntityType("适用条件", "applicable_condition", "structure"),
    "政策对象": EntityType("政策对象", "policy_target_group", "structure"),
    "项目": EntityType("项目", "project", "structure"),
    "政策背景": EntityType("政策背景", "policy_background", "semantic"),
    "政策举措": EntityType("政策举措", "policy_action", "semantic"),
    "政策目标": EntityType("政策目标", "policy_goal", "semantic"),
    "领域主题": EntityType("领域主题", "domain_topic", "global"),
    "机构": EntityType("机构", "organization", "global"),
    "管辖区域": EntityType("管辖区域", "jurisdiction", "global"),
    "时间区间": EntityType("时间区间", "time_period", "global"),
}


LEVEL_TO_ENTITY_TYPES: Dict[str, List[str]] = {
    "global": ["政策", "机构", "管辖区域", "时间区间", "领域主题"],
    "structure": ["政策条文", "项目", "政策对象", "适用条件"],
    "semantic": ["政策背景", "政策目标", "政策举措", "政策工具"],
}

# 关系类型占位；后续可按你的正式定义扩展
RELATION_TYPES: List[str] = [
    "发布于",
    "由...发布",
    "面向对象",
    "包含条文",
    "包含项目",
    "适用于",
    "支持目标",
    "采用工具",
    "提出举措",
    "基于背景",
    "关联主题",
]
