def generate_ideas_prompt(topic: str, description: str | None, number_of_ideas: int) -> str:
    return f"""
Ты эксперт по структурированному брейнштормингу.
Сгенерируй ровно {number_of_ideas} идей по теме: "{topic}".
Дополнительное описание: "{description or 'Нет'}".

Ответ ТОЛЬКО в виде JSON-массива без markdown:
[
  {{
    "title": "Короткий заголовок",
    "description": "Содержательное описание идеи"
  }}
]
"""


def six_hats_prompt(topic: str, idea_title: str, idea_description: str) -> str:
    return f"""
Проанализируй идею по методу Шести шляп мышления.
Тема: "{topic}".
Идея: "{idea_title}".
Описание идеи: "{idea_description}".

Верни строго JSON-объект без markdown:
{{
  "white": "Факты и данные",
  "red": "Эмоции и интуиция",
  "black": "Риски и ограничения",
  "yellow": "Преимущества и ценность",
  "green": "Улучшения и альтернативы",
  "blue": "Вывод и следующие шаги"
}}
"""


def score_prompt(topic: str, idea_title: str, idea_description: str, analysis_json: dict) -> str:
    return f"""
Оцени идею по шкале 0-10 по 3 критериям:
- novelty (новизна)
- feasibility (реализуемость)
- usefulness (полезность)

Тема: "{topic}"
Идея: "{idea_title}"
Описание: "{idea_description}"
Анализ: {analysis_json}

Верни строго JSON-объект без markdown:
{{
  "novelty": 0,
  "feasibility": 0,
  "usefulness": 0,
  "total": 0
}}

Где total = novelty + feasibility + usefulness.
"""
