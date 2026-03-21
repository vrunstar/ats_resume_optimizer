from src.gemini_client import get_model
from src.parser import extract_json
from src.prompt import KEYWORD_PROMPT

def extract_keywords(job_description: str) -> dict:
    model = get_model()
    prompt = KEYWORD_PROMPT.format(job_description = job_description)
    response = model.generate_content(prompt)
    content = response.text if hasattr(response, "text") else str(response)
    return extract_json(content)