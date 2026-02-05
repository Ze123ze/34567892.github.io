from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List


@dataclass(frozen=True)
class EntityType:
    chinese_name: str
    english_name: str
    level: str
    data_properties: List[str]


ENTITY_TYPES: Dict[str, EntityType] = {
    "政策": EntityType(
        "政策",
        "Policy",
        "global",
        [
            "policyId",
            "title",
            "documentNumber",
            "issuingAuthority",
            "effectiveDate",
            "expiryDate",
            "policyType",
            "fullText",
            "defaultAnalysisLayer",
        ],
    ),
    "机构": EntityType("机构", "Organization", "global", ["orgId", "name", "type", "jurisdiction"]),
    "管辖区域": EntityType("管辖区域", "Jurisdiction", "global", ["ocean", "country", "continent"]),
    "时间区间": EntityType("时间区间", "TimePeriod", "global", ["startDate", "endDate"]),
    "领域主题": EntityType("领域主题", "DomainTheme", "global", ["themeId", "themeLabel"]),
    "政策条文": EntityType("政策条文", "Provision", "structure", ["provisionId", "paragraphNumber", "textContent"]),
    "项目": EntityType(
        "项目",
        "Project",
        "structure",
        ["projectId", "name", "country", "nature", "description", "defaultAnalysisLayer"],
    ),
    "政策对象": EntityType("政策对象", "PolicyTarget", "structure", ["targetId", "name", "country", "targetType"]),
    "适用条件": EntityType("适用条件", "EligibilityCondition", "structure", ["conditionText"]),
    "政策背景": EntityType(
        "政策背景",
        "PolicyBackground",
        "semantic",
        ["annotationId", "defaultAnalysisLayer", "keywords", "summary"],
    ),
    "政策举措": EntityType(
        "政策举措",
        "PolicyInitiative",
        "semantic",
        ["annotationId", "defaultAnalysisLayer", "keywords", "summary"],
    ),
    "政策目标": EntityType(
        "政策目标",
        "PolicyObjective",
        "semantic",
        ["annotationId", "defaultAnalysisLayer", "keywords", "summary"],
    ),
    "政策工具": EntityType("政策工具", "PolicyTool", "semantic", ["toolId", "toolType", "defaultAnalysisLayer"]),
}


LEVEL_TO_ENTITY_TYPES: Dict[str, List[str]] = {
    "global": ["政策", "机构", "管辖区域", "时间区间", "领域主题"],
    "structure": ["政策条文", "项目", "政策对象", "适用条件"],
    "semantic": ["政策背景", "政策目标", "政策举措", "政策工具"],
}


RELATION_TYPES: List[str] = [
    # Policy
    "hasProvision",
    "hasPolicyTool",
    "supportsProject",
    "hasBackgroundAnnotation",
    "hasInitiativeAnnotation",
    "hasObjectiveAnnotation",
    "coversTheme",
    "appliesTo",
    "cites",
    # Provision
    "belongsToPolicy",
    "isSourceOf",
    # PolicyTool / EligibilityCondition / PolicyTarget
    "appliesToProvision",
    "hasEligibilityCondition",
    "appliesToTarget",
    "isSubjectInProvision",
    "isObjectInProvision",
    "satisfiesCondition",
    # Project
    "supportedByPolicy",
    "implementedBy",
    "coversTimePeriod",
    # Semantic annotations
    "sourceProvision",
    # DomainTheme
    "appliesToPolicy",
    "hasSubTheme",
    # Organization / Jurisdiction
    "hasJurisdictionOver",
    "isJurisdictedBy",
]


RELATION_CONSTRAINTS: Dict[str, Dict[str, List[str]]] = {
    "hasProvision": {"head": ["政策"], "tail": ["政策条文"]},
    "hasPolicyTool": {"head": ["政策"], "tail": ["政策工具"]},
    "supportsProject": {"head": ["政策"], "tail": ["项目"]},
    "hasBackgroundAnnotation": {"head": ["政策"], "tail": ["政策背景"]},
    "hasInitiativeAnnotation": {"head": ["政策"], "tail": ["政策举措"]},
    "hasObjectiveAnnotation": {"head": ["政策"], "tail": ["政策目标"]},
    "coversTheme": {"head": ["政策"], "tail": ["领域主题"]},
    "appliesTo": {"head": ["政策"], "tail": ["管辖区域"]},
    "belongsToPolicy": {"head": ["政策条文"], "tail": ["政策"]},
    "appliesToProvision": {"head": ["政策工具"], "tail": ["政策条文"]},
    "hasEligibilityCondition": {"head": ["政策工具"], "tail": ["适用条件"]},
    "appliesToTarget": {"head": ["适用条件"], "tail": ["政策对象"]},
    "isSubjectInProvision": {"head": ["政策对象"], "tail": ["政策条文"]},
    "isObjectInProvision": {"head": ["政策对象"], "tail": ["政策条文"]},
    "satisfiesCondition": {"head": ["政策对象"], "tail": ["适用条件"]},
    "supportedByPolicy": {"head": ["项目"], "tail": ["政策"]},
    "implementedBy": {"head": ["项目"], "tail": ["机构"]},
    "coversTimePeriod": {"head": ["项目"], "tail": ["时间区间"]},
    "sourceProvision": {"head": ["政策背景", "政策举措", "政策目标"], "tail": ["政策条文"]},
    "appliesToPolicy": {"head": ["领域主题"], "tail": ["政策"]},
    "hasSubTheme": {"head": ["领域主题"], "tail": ["领域主题"]},
    "hasJurisdictionOver": {"head": ["机构"], "tail": ["管辖区域"]},
    "isJurisdictedBy": {"head": ["管辖区域"], "tail": ["机构"]},
}
