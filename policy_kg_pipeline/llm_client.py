from __future__ import annotations

import json
import os
from typing import Any, Dict, List

import httpx
from dotenv import load_dotenv

load_dotenv()


class LLMClient:
    def __init__(self) -> None:
        self.base_url = os.getenv("LLM_BASE_URL", "https://api.openai.com/v1").rstrip("/")
        self.api_key = os.getenv("LLM_API_KEY", "")
        self.model = os.getenv("LLM_MODEL", "gpt-4o-mini")
        self.timeout = int(os.getenv("LLM_TIMEOUT_SECONDS", "120"))

    async def chat_json(self, system_prompt: str, user_prompt: str) -> Dict[str, Any]:
        url = f"{self.base_url}/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        payload: Dict[str, Any] = {
            "model": self.model,
            "temperature": 0,
            "response_format": {"type": "json_object"},
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
        }

        async with httpx.AsyncClient(timeout=self.timeout) as client:
            resp = await client.post(url, headers=headers, json=payload)
            resp.raise_for_status()
            data = resp.json()

        content = data["choices"][0]["message"]["content"]
        try:
            return json.loads(content)
        except json.JSONDecodeError:
            return {"raw": content}


def build_context_block(doc_id: str, title: str | None, text: str) -> str:
    title_part = title or "(无标题)"
    return f"doc_id: {doc_id}\ntitle: {title_part}\n\n正文:\n{text}"


def compact_entities_for_prompt(entities: List[Dict[str, Any]]) -> str:
    if not entities:
        return "[]"
    return json.dumps(entities, ensure_ascii=False, indent=2)
