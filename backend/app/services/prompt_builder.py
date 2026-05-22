from dataclasses import dataclass


@dataclass
class PromptBuilderInput:
    topic: str
    role: str | None = None
    context: str | None = None
    constraints: str | None = None
    environment: str | None = None
    requirements: str | None = None
    additional_info: str | None = None
    output_format: str | None = None


def build_gps_prompt(data: PromptBuilderInput) -> str:
    role = (data.role or "Senior innovation strategist and product architect").strip()
    context = (data.context or "No additional context provided").strip()
    constraints = (data.constraints or "No strict constraints provided").strip()
    environment = (data.environment or "General market environment").strip()
    requirements = (data.requirements or "No extra requirements provided").strip()
    additional_info = (data.additional_info or "None").strip()
    output_format = (
        data.output_format
        or """
Return ONLY valid JSON array:
[
  {
    "title": "Short idea title",
    "description": "Detailed idea description"
  }
]
""".strip()
    )

    return f"""
ROLE:
{role}

TASK / PROBLEM:
Generate high-quality product or business ideas for topic: "{data.topic.strip()}".

CONTEXT:
{context}

CONSTRAINTS:
{constraints}

ENVIRONMENT:
{environment}

REQUIREMENTS:
{requirements}

ADDITIONAL INFO:
{additional_info}

OUTPUT FORMAT:
{output_format}
""".strip()
