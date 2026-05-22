from sqlalchemy.orm import Session

from app.core.config import settings
from app.models.entities import AdminLog, AppSetting
from app.services.llm_models import LLM_MODEL_OPTIONS, resolve_openrouter_model
from app.services.prompt_store import (
    PROMPT_TYPES,
    get_prompt_template,
    save_prompt_template,
    seed_prompts_if_empty,
)

SETTINGS_LLM_MODEL_KEY = "llm_model"
DEFAULT_LLM_MODEL = "Laguna M.1"


def verify_admin_password(password: str) -> bool:
    expected = (settings.admin_password or "").strip()
    if not expected:
        return False
    return password == expected


def seed_admin_defaults(db: Session) -> None:
    seed_prompts_if_empty(db)
    row = db.query(AppSetting).filter(AppSetting.key == SETTINGS_LLM_MODEL_KEY).one_or_none()
    if row is None:
        db.add(AppSetting(key=SETTINGS_LLM_MODEL_KEY, value=DEFAULT_LLM_MODEL))
        db.commit()


def get_llm_model_display(db: Session) -> str:
    row = db.query(AppSetting).filter(AppSetting.key == SETTINGS_LLM_MODEL_KEY).one_or_none()
    if row and row.value.strip():
        return row.value.strip()
    return DEFAULT_LLM_MODEL


def set_llm_model_display(db: Session, model_name: str) -> str:
    name = model_name.strip()
    if name not in LLM_MODEL_OPTIONS:
        raise ValueError(f"Неизвестная модель: {name}")
    row = db.query(AppSetting).filter(AppSetting.key == SETTINGS_LLM_MODEL_KEY).one_or_none()
    if row is None:
        db.add(AppSetting(key=SETTINGS_LLM_MODEL_KEY, value=name))
    else:
        row.value = name
    db.commit()
    return name


def resolve_model_for_request(db: Session) -> str:
    from app.core.config import settings as app_settings

    display = get_llm_model_display(db)
    return resolve_openrouter_model(display, app_settings.openrouter_model)


def get_all_prompts(db: Session) -> dict[str, str]:
    return {prompt_type: get_prompt_template(db, prompt_type) for prompt_type in PROMPT_TYPES}


def save_prompts(db: Session, payloads: dict[str, str]) -> dict[str, str]:
    for prompt_type, content in payloads.items():
        if prompt_type not in PROMPT_TYPES:
            raise ValueError(f"Неизвестный тип промта: {prompt_type}")
        if not content.strip():
            raise ValueError(f"Промт «{prompt_type}» не может быть пустым")
        save_prompt_template(db, prompt_type, content)
    return get_all_prompts(db)


def log_event(db: Session, action: str, details: str) -> AdminLog:
    entry = AdminLog(action=action, details=details[:4000])
    db.add(entry)
    db.commit()
    db.refresh(entry)
    return entry


def list_logs(db: Session, limit: int = 100) -> list[AdminLog]:
    safe_limit = max(1, min(limit, 500))
    return (
        db.query(AdminLog)
        .order_by(AdminLog.timestamp.desc(), AdminLog.id.desc())
        .limit(safe_limit)
        .all()
    )
