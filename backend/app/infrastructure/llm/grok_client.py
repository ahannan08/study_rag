import json
import re
from typing import Any

import httpx

from app.config import get_settings

XAI_CHAT_URL = "https://api.x.ai/v1/chat/completions"
GROQ_CHAT_URL = "https://api.groq.com/openai/v1/chat/completions"


class GrokClient:
    """Chat completions client for Groq (console.groq.com) or xAI Grok (console.x.ai)."""

    def __init__(self) -> None:
        self.settings = get_settings()

    def _resolve(self) -> tuple[str, str, str]:
        """Return (api_url, model, api_key)."""
        s = self.settings
        groq_key = (s.groq_api_key or "").strip()
        xai_key = (s.xai_api_key or "").strip()

        # Legacy: Groq key stored in XAI_API_KEY
        if not groq_key and xai_key.startswith("gsk_"):
            groq_key = xai_key

        provider = s.llm_provider.lower()
        if provider == "auto":
            if groq_key:
                provider = "groq"
            elif xai_key:
                provider = "xai"
            else:
                provider = ""

        if provider == "groq":
            if not groq_key:
                raise RuntimeError("GROQ_API_KEY is not configured (get a gsk_ key at console.groq.com)")
            return GROQ_CHAT_URL, s.groq_model, groq_key

        if provider == "xai":
            if not xai_key or xai_key.startswith("gsk_"):
                raise RuntimeError("XAI_API_KEY is not configured (get an xai- key at console.x.ai)")
            return XAI_CHAT_URL, s.xai_model, xai_key

        raise RuntimeError(
            "No LLM configured. Set GROQ_API_KEY + GROQ_MODEL (Groq) or XAI_API_KEY + XAI_MODEL (xAI)."
        )

    def chat_json(self, system: str, user: str) -> Any:
        url, model, key = self._resolve()
        headers = {
            "Authorization": f"Bearer {key}",
            "Content-Type": "application/json",
        }
        body = {
            "model": model,
            "messages": [
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
            "temperature": 0.2,
        }
        with httpx.Client(timeout=self.settings.grok_timeout_seconds) as client:
            resp = client.post(url, headers=headers, json=body)
            if resp.is_error:
                raise RuntimeError(f"LLM API {resp.status_code} ({model}): {resp.text[:800]}")
            content = resp.json()["choices"][0]["message"]["content"]
        return _parse_json_content(content)


def _parse_json_content(content: str) -> Any:
    content = content.strip()
    if content.startswith("```"):
        content = re.sub(r"^```(?:json)?\s*", "", content)
        content = re.sub(r"\s*```$", "", content)
    return json.loads(content)
