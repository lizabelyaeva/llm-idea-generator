from fastapi import APIRouter, Depends, Header, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.core.config import settings
from app.db.session import get_db
from app.services.auth import create_admin_token, verify_admin_token
from app.schemas.admin import (
    AdminAuthRequest,
    AdminAuthResponse,
    AdminLogsResponse,
    AdminLogItem,
    AdminPromptsResponse,
    AdminPromptsUpdateRequest,
    AdminSettingsResponse,
    AdminSettingsUpdateRequest,
)
from app.services.admin_service import (
    get_all_prompts,
    get_llm_model_display,
    list_logs,
    save_prompts,
    set_llm_model_display,
    verify_admin_password,
)
from app.services.llm_models import LLM_MODEL_OPTIONS

router = APIRouter(prefix="/admin", tags=["admin"])
admin_bearer = HTTPBearer(auto_error=False)


def require_admin_access(
    creds: HTTPAuthorizationCredentials | None = Depends(admin_bearer),
    x_admin_password: str | None = Header(default=None, alias="X-Admin-Password"),
) -> None:
    if not (settings.admin_password or "").strip():
        raise HTTPException(status_code=503, detail="ADMIN_PASSWORD не задан в .env")
    if creds and creds.credentials and verify_admin_token(creds.credentials):
        return
    if x_admin_password and verify_admin_password(x_admin_password):
        return
    raise HTTPException(status_code=401, detail="Требуется авторизация администратора")


@router.post("/auth", response_model=AdminAuthResponse)
def admin_auth(request: AdminAuthRequest):
    if not verify_admin_password(request.password):
        raise HTTPException(status_code=401, detail="Неверный пароль администратора")
    return AdminAuthResponse(ok=True, admin_token=create_admin_token())


@router.get("/settings", response_model=AdminSettingsResponse, dependencies=[Depends(require_admin_access)])
def get_settings(db: Session = Depends(get_db)):
    return AdminSettingsResponse(
        llm_model=get_llm_model_display(db),
        available_models=LLM_MODEL_OPTIONS,
    )


@router.post("/settings", response_model=AdminSettingsResponse, dependencies=[Depends(require_admin_access)])
def update_settings(request: AdminSettingsUpdateRequest, db: Session = Depends(get_db)):
    try:
        set_llm_model_display(db, request.llm_model)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return AdminSettingsResponse(
        llm_model=get_llm_model_display(db),
        available_models=LLM_MODEL_OPTIONS,
    )


@router.get("/prompts", response_model=AdminPromptsResponse, dependencies=[Depends(require_admin_access)])
def get_prompts(db: Session = Depends(get_db)):
    data = get_all_prompts(db)
    return AdminPromptsResponse(
        generation=data["generation"],
        analysis=data["analysis"],
        evaluation=data["evaluation"],
    )


@router.post("/prompts", response_model=AdminPromptsResponse, dependencies=[Depends(require_admin_access)])
def update_prompts(request: AdminPromptsUpdateRequest, db: Session = Depends(get_db)):
    payload = {
        key: value
        for key, value in {
            "generation": request.generation,
            "analysis": request.analysis,
            "evaluation": request.evaluation,
        }.items()
        if value is not None
    }
    if not payload:
        raise HTTPException(status_code=400, detail="Нет полей для сохранения")
    try:
        data = save_prompts(db, payload)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return AdminPromptsResponse(
        generation=data["generation"],
        analysis=data["analysis"],
        evaluation=data["evaluation"],
    )


@router.get("/logs", response_model=AdminLogsResponse, dependencies=[Depends(require_admin_access)])
def get_logs(limit: int = 100, db: Session = Depends(get_db)):
    rows = list_logs(db, limit=limit)
    return AdminLogsResponse(items=[AdminLogItem.model_validate(row) for row in rows])
