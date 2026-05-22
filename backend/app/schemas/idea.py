from typing import Optional

from pydantic import BaseModel, Field


class GenerateRequest(BaseModel):
    topic: str = Field(..., min_length=3, max_length=500)
    description: Optional[str] = Field(default=None, max_length=2000)
    number_of_ideas: int = Field(default=5, ge=1, le=15)


class IdeaDraft(BaseModel):
    title: str
    description: str


class HatsAnalysis(BaseModel):
    white: str
    red: str
    black: str
    yellow: str
    green: str
    blue: str


class IdeaScore(BaseModel):
    novelty: float = Field(ge=0, le=10)
    feasibility: float = Field(ge=0, le=10)
    usefulness: float = Field(ge=0, le=10)
    total: float


class AnalyzeRequest(BaseModel):
    idea_id: int


class ScoreRequest(BaseModel):
    idea_id: int


class IdeaResponse(BaseModel):
    id: int
    title: str
    description: str
    rank: Optional[int]
    analysis: Optional[HatsAnalysis]
    score: Optional[IdeaScore]
    session_id: int
    session_topic: str

    class Config:
        from_attributes = True


class GenerateResponse(BaseModel):
    session_id: int
    ideas: list[IdeaResponse]
