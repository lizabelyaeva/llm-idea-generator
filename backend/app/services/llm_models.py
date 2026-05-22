"""Display names for admin UI and mapping to OpenRouter model slugs."""

LLM_MODEL_OPTIONS: list[str] = [
    "Nemotron 3 Super",
    "Laguna M.1",
    "gpt-oss-120b",
    "GLM 4.5 Air",
    "DeepSeek V4 Flash",
    "Trinity Large Thinking",
    "Laguna XS.2",
    "MiniMax M2.5",
    "Nemotron Nano 30B",
    "gpt-oss-20b",
    "CoBuddy",
    "Gemma 4 31B",
    "Llama 3.3 70B",
]

# Slugs may be adjusted in OpenRouter; unknown names are sent as-is.
LLM_MODEL_MAP: dict[str, str] = {
    "Nemotron 3 Super": "nvidia/nemotron-3-super",
    "Laguna M.1": "openrouter/auto",
    "gpt-oss-120b": "openai/gpt-oss-120b",
    "GLM 4.5 Air": "z-ai/glm-4.5-air",
    "DeepSeek V4 Flash": "deepseek/deepseek-v4-flash",
    "Trinity Large Thinking": "arcee-ai/trinity-large-thinking",
    "Laguna XS.2": "openrouter/auto",
    "MiniMax M2.5": "minimax/minimax-m2.5",
    "Nemotron Nano 30B": "nvidia/nemotron-nano-30b",
    "gpt-oss-20b": "openai/gpt-oss-20b",
    "CoBuddy": "openrouter/auto",
    "Gemma 4 31B": "google/gemma-4-31b",
    "Llama 3.3 70B": "meta-llama/llama-3.3-70b-instruct",
}


def resolve_openrouter_model(display_name: str, fallback: str) -> str:
    name = (display_name or "").strip()
    if not name:
        return fallback
    return LLM_MODEL_MAP.get(name, name)
