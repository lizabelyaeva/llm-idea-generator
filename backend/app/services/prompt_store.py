import json
from typing import Any

from sqlalchemy.orm import Session

from app.models.entities import PromptTemplate
from app.services.prompts import generate_ideas_prompt, six_hats_prompt

PROMPT_GENERATION = "generation"
PROMPT_ANALYSIS = "analysis"
PROMPT_EVALUATION = "evaluation"

PROMPT_TYPES = (PROMPT_GENERATION, PROMPT_ANALYSIS, PROMPT_EVALUATION)

PLACEHOLDER_KEYS = (
    "base_prompt",
    "number_of_ideas",
    "topic",
    "idea_title",
    "idea_description",
    "analysis_json",
    "all_ideas_json",
)


def _default_evaluation_template() -> str:
    return """
Оцени идею по критериям novelty, feasibility, usefulness (шкала 0-10).

Тема: "{topic}"
Идея: "{idea_title}"
Описание: "{idea_description}"
Анализ: {analysis_json}

Верни JSON:

{
  "title": "{idea_title}",
  "novelty": 0,
  "feasibility": 0,
  "usefulness": 0,
  "confidence": 0.5,
  "justification": "краткое обоснование оценки"
}
""".strip()


def default_prompt_templates() -> dict[str, str]:
    sample_base = "ROLE: strategist\nTASK: ideas for «тема»"
    generation_body = generate_ideas_prompt(sample_base, 3)
    generation_template = generation_body.replace(sample_base, "{base_prompt}")
    analysis_template = six_hats_prompt("{topic}", "{idea_title}", "{idea_description}")
    return {
        PROMPT_GENERATION: generation_template,
        PROMPT_ANALYSIS: analysis_template,
        PROMPT_EVALUATION: _default_evaluation_template(),
    }


def seed_prompts_if_empty(db: Session) -> None:
    if db.query(PromptTemplate).count() > 0:
        return
    for prompt_type, content in default_prompt_templates().items():
        db.add(PromptTemplate(type=prompt_type, content=content))
    db.commit()


def reset_prompts_to_defaults(db: Session) -> None:
    """Восстанавливает шаблоны промтов из кода (после поломки format() в админке)."""
    defaults = default_prompt_templates()
    for prompt_type, content in defaults.items():
        row = db.query(PromptTemplate).filter(PromptTemplate.type == prompt_type).one_or_none()
        if row is None:
            db.add(PromptTemplate(type=prompt_type, content=content))
        else:
            row.content = content
    db.commit()


def get_prompt_template(db: Session, prompt_type: str) -> str:
    row = db.query(PromptTemplate).filter(PromptTemplate.type == prompt_type).one_or_none()
    defaults = default_prompt_templates()
    if row is not None:
        return row.content
    return defaults[prompt_type]


def save_prompt_template(db: Session, prompt_type: str, content: str) -> None:
    row = db.query(PromptTemplate).filter(PromptTemplate.type == prompt_type).one_or_none()
    if row is None:
        db.add(PromptTemplate(type=prompt_type, content=content))
    else:
        row.content = content
    db.commit()


def _value_to_text(value: Any) -> str:
    if isinstance(value, str):
        return value
    if value is None:
        return ""
    return json.dumps(value, ensure_ascii=False)


def _apply_placeholders(template: str, values: dict[str, Any]) -> str:
    """Подставляет только известные {ключи}, не трогая фигурные скобки в примерах JSON."""
    result = template
    for key in PLACEHOLDER_KEYS:
        if key not in values:
            continue
        token = "{" + key + "}"
        if token in result:
            result = result.replace(token, _value_to_text(values[key]))
    # Литералы {{ }} из старых шаблонов оценки → обычные { }
    return result.replace("{{", "{").replace("}}", "}")


def render_generation_prompt(db: Session, base_prompt: str, number_of_ideas: int) -> str:
    template = get_prompt_template(db, PROMPT_GENERATION)
    return _apply_placeholders(
        template,
        {"base_prompt": base_prompt, "number_of_ideas": number_of_ideas},
    )


def render_analysis_prompt(db: Session, topic: str, idea_title: str, idea_description: str) -> str:
    template = get_prompt_template(db, PROMPT_ANALYSIS)
    return _apply_placeholders(
        template,
        {
            "topic": topic,
            "idea_title": idea_title,
            "idea_description": idea_description,
        },
    )


def render_evaluation_prompt(
    db: Session,
    topic: str,
    idea_title: str,
    idea_description: str,
    analysis: dict | list | None,
) -> str:
    template = get_prompt_template(db, PROMPT_EVALUATION)
    if "{all_ideas_json}" in template and "{topic}" not in template:
        payload = [
            {
                "title": idea_title,
                "description": idea_description,
                "analysis": analysis,
            }
        ]
        return _apply_placeholders(template, {"all_ideas_json": payload})

    return _apply_placeholders(
        template,
        {
            "topic": topic,
            "idea_title": idea_title,
            "idea_description": idea_description,
            "analysis_json": analysis or {},
        },
    )
