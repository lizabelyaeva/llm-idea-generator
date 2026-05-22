from datetime import datetime

from pydantic import BaseModel, Field


class AdminAuthRequest(BaseModel):
    password: str


class AdminAuthResponse(BaseModel):
    ok: bool = True
    admin_token: str


class AdminSettingsResponse(BaseModel):
    llm_model: str
    available_models: list[str]


class AdminSettingsUpdateRequest(BaseModel):
    llm_model: str


class AdminPromptsResponse(BaseModel):
    generation: str
    analysis: str
    evaluation: str


class AdminPromptsUpdateRequest(BaseModel):
    generation: str | None = None
    analysis: str | None = None
    evaluation: str | None = None


class AdminLogItem(BaseModel):
    id: int
    action: str
    timestamp: datetime
    details: str

    model_config = {"from_attributes": True}


class AdminLogsResponse(BaseModel):
    items: list[AdminLogItem] = Field(default_factory=list)
