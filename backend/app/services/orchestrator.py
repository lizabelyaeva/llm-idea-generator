import json

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.entities import Analysis, Idea, Session as IdeaSession
from app.schemas.idea import GenerateRequest
from app.services.llm_service import OpenRouterService
from app.services.prompts import generate_ideas_prompt, score_prompt, six_hats_prompt


class IdeaOrchestrator:
    @staticmethod
    def _as_text(value: object) -> str:
        if isinstance(value, str):
            return value
        if value is None:
            return ""
        # Иногда LLM возвращает вложенный JSON вместо строки.
        return json.dumps(value, ensure_ascii=False)

    @staticmethod
    def _as_float(value: object, default: float = 0.0) -> float:
        try:
            return float(value)
        except (TypeError, ValueError):
            return default

    def __init__(self, db: Session):
        self.db = db
        self.llm = OpenRouterService()

    async def run_full_pipeline(self, request: GenerateRequest) -> tuple[int, list[Idea]]:
        draft_prompt = generate_ideas_prompt(
            request.topic,
            request.description,
            request.number_of_ideas,
        )
        generated = await self.llm.ask_json(draft_prompt)
        if not isinstance(generated, list):
            raise HTTPException(status_code=502, detail="Ожидался JSON-массив идей от LLM")

        session = IdeaSession(
            topic=request.topic,
            description=request.description,
            ideas_requested=request.number_of_ideas,
        )
        self.db.add(session)
        self.db.flush()

        ideas: list[Idea] = []
        for item in generated[: request.number_of_ideas]:
            idea = Idea(
                title=item.get("title", "Без названия"),
                description=item.get("description", ""),
                session_id=session.id,
            )
            self.db.add(idea)
            self.db.flush()

            analysis = await self.analyze_idea(request.topic, idea)
            score = await self.score_idea(request.topic, idea, analysis)

            idea.total_score = float(score["total"])
            idea.score = score
            ideas.append(idea)

        ranked = sorted(ideas, key=lambda i: i.total_score or 0, reverse=True)
        for idx, idea in enumerate(ranked, start=1):
            idea.rank = idx

        self.db.commit()
        for idea in ranked:
            self.db.refresh(idea)
        return session.id, ranked

    async def analyze_idea(self, topic: str, idea: Idea) -> dict:
        result = await self.llm.ask_json(six_hats_prompt(topic, idea.title, idea.description))
        if not isinstance(result, dict):
            raise HTTPException(status_code=502, detail="Ожидался JSON-объект анализа")
        normalized = {
            "white": self._as_text(result.get("white")),
            "red": self._as_text(result.get("red")),
            "black": self._as_text(result.get("black")),
            "yellow": self._as_text(result.get("yellow")),
            "green": self._as_text(result.get("green")),
            "blue": self._as_text(result.get("blue")),
        }
        analysis = self.db.query(Analysis).filter(Analysis.idea_id == idea.id).one_or_none()
        if analysis is None:
            analysis = Analysis(idea_id=idea.id, **normalized)
            self.db.add(analysis)
        else:
            analysis.white = normalized["white"]
            analysis.red = normalized["red"]
            analysis.black = normalized["black"]
            analysis.yellow = normalized["yellow"]
            analysis.green = normalized["green"]
            analysis.blue = normalized["blue"]
        self.db.flush()
        return normalized

    async def score_idea(self, topic: str, idea: Idea, analysis: dict | None = None) -> dict:
        if analysis is None:
            if not idea.analysis:
                raise HTTPException(status_code=400, detail="Сначала выполните анализ идеи")
            analysis = {
                "white": idea.analysis.white,
                "red": idea.analysis.red,
                "black": idea.analysis.black,
                "yellow": idea.analysis.yellow,
                "green": idea.analysis.green,
                "blue": idea.analysis.blue,
            }

        result = await self.llm.ask_json(score_prompt(topic, idea.title, idea.description, analysis))
        if not isinstance(result, dict):
            raise HTTPException(status_code=502, detail="Ожидался JSON-объект оценки")
        normalized = {
            "novelty": self._as_float(result.get("novelty")),
            "feasibility": self._as_float(result.get("feasibility")),
            "usefulness": self._as_float(result.get("usefulness")),
        }
        normalized["total"] = round(
            normalized["novelty"] + normalized["feasibility"] + normalized["usefulness"],
            2,
        )
        idea.score = normalized
        idea.total_score = normalized["total"]
        self.db.flush()
        return normalized
