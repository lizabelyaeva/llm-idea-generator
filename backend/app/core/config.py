from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "AI Лаборатория Идей"
    database_url: str = "postgresql+psycopg://postgres:postgres@localhost:5432/idea_lab"
    openrouter_api_key: str = ""
    openrouter_base_url: str = "https://openrouter.ai/api/v1/chat/completions"
    openrouter_model: str = "mistralai/mistral-7b-instruct:free"
    request_timeout_seconds: int = 60

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )


settings = Settings()
