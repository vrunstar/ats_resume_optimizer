from src.gemini_client import get_model
from src.parser import extract_json
from src.prompt import OPTIMIZE_PROMPT

def optimize_resume(job_description: str, resume_text: str, keywords: list[str]) -> dict:
    model = get_model()
    prompt = OPTIMIZE_PROMPT.format(
        job_description = job_description,
        keywords=", ".join(keywords),
        resume_text=resume_text
    )
    response = model.generate_content(prompt)
    content = response.text if hasattr(response, "text") else str(response)
    return extract_json(content)