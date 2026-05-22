import json

import httpx
from fastapi import HTTPException

from app.core.config import settings


class OpenRouterService:
    def __init__(self) -> None:
        self.api_key = (settings.openrouter_api_key or "").strip()
        if not self.api_key:
            raise HTTPException(status_code=500, detail="OPENROUTER_API_KEY не задан в .env")

    async def ask_json(self, prompt: str) -> dict | list:
        payload = {
            "model": settings.openrouter_model,
            "messages": [
                {
                    "role": "system",
                    "content": "Ты отвечаешь только валидным JSON без markdown и без комментариев.",
                },
                {"role": "user", "content": prompt},
            ],
            "temperature": 0.4,
        }
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        try:
            async with httpx.AsyncClient(timeout=settings.request_timeout_seconds) as client:
                response = await client.post(settings.openrouter_base_url, headers=headers, json=payload)
        except httpx.ReadTimeout as exc:
            raise HTTPException(status_code=504, detail="OpenRouter не ответил вовремя, попробуйте снова") from exc
        except httpx.HTTPError as exc:
            raise HTTPException(status_code=502, detail=f"Сетевая ошибка при запросе к OpenRouter: {exc}") from exc
        if response.status_code >= 400:
            raise HTTPException(status_code=502, detail=f"Ошибка OpenRouter: {response.text}")
        content = response.json()["choices"][0]["message"]["content"]
        try:
            return json.loads(content)
        except json.JSONDecodeError as exc:
            raise HTTPException(status_code=502, detail=f"LLM вернул невалидный JSON: {content}") from exc
