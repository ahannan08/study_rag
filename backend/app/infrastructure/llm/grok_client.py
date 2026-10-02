import json
import re
from typing import Any

import httpx

from app.config import get_settings


class GrokClient:
    def __init__(self) -> None:
        self.settings = get_settings()

    def chat_json(self, system: str, user: str) -> Any:
        if not self.settings.xai_api_key:
            raise RuntimeError("XAI_API_KEY is not configured")
        url = "https://api.x.ai/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.settings.xai_api_key}",
            "Content-Type": "application/json",
        }
        body = {
            "model": self.settings.xai_model,
            "messages": [
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
            "temperature": 0.2,
        }
        with httpx.Client(timeout=self.settings.grok_timeout_seconds) as client:
            resp = client.post(url, headers=headers, json=body)
            resp.raise_for_status()
            content = resp.json()["choices"][0]["message"]["content"]
        return _parse_json_content(content)


def _parse_json_content(content: str) -> Any:
    content = content.strip()
    if content.startswith("```"):
        content = re.sub(r"^```(?:json)?\s*", "", content)
        content = re.sub(r"\s*```$", "", content)
    return json.loads(content)
