import os
import re
import json
import time

from dotenv import load_dotenv
from groq import Groq

from src.prompt import KEYWORD_PROMPT, build_analyse_prompt

load_dotenv()

_API_KEY     = os.getenv("GROQ_API_KEY")
_MODEL       = "llama-3.3-70b-versatile"
_MAX_RETRIES = 3
_RETRY_DELAY = 2

if not _API_KEY:
    raise ValueError("GROQ_API_KEY is not set. Add it to your .env file.")

_client = Groq(api_key=_API_KEY)


# ─────────────────────────────────────────────
# Internal: API call with retry
# ─────────────────────────────────────────────

def _call(prompt: str, max_tokens: int = 4096) -> str:
    last_err = None
    for attempt in range(1, _MAX_RETRIES + 1):
        try:
            response = _client.chat.completions.create(
                model=_MODEL,
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are a JSON API. Respond with a valid JSON object only. "
                            "No explanations, no markdown fences, no prose — raw JSON only."
                        ),
                    },
                    {"role": "user", "content": prompt},
                ],
                max_tokens=max_tokens,
                temperature=0.2,
                response_format={"type": "json_object"},
            )
            return response.choices[0].message.content
        except Exception as e:
            last_err = e
            err_str = str(e)
            if "429" in err_str or "rate" in err_str.lower() or "quota" in err_str.lower():
                raise RuntimeError(
                    "Groq rate limit hit. Wait a moment and try again, "
                    "or check your limits at console.groq.com"
                )
            if attempt < _MAX_RETRIES:
                time.sleep(_RETRY_DELAY * attempt)
    raise RuntimeError(
        f"Groq API unavailable after {_MAX_RETRIES} attempts. Last error: {last_err}"
    )


# ─────────────────────────────────────────────
# Internal: JSON parsing
# ─────────────────────────────────────────────

def _parse_json(raw: str) -> dict:
    text = re.sub(r"```(?:json)?\s*", "", raw.strip(), flags=re.IGNORECASE)
    text = re.sub(r"```", "", text).strip()
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass
    match = re.search(r"\{.*\}", text, re.DOTALL)
    if match:
        candidate = re.sub(r",\s*([\}\]])", r"\1", match.group(0))
        try:
            return json.loads(candidate)
        except json.JSONDecodeError:
            pass
    raise ValueError(f"Could not parse JSON from model response.\nRaw (first 600):\n{raw[:600]}")


# ─────────────────────────────────────────────
# Public: keyword extraction
# ─────────────────────────────────────────────

_EMPTY_KEYWORDS = {
    "target_role": "",
    "keywords":    [],
    "skills":      [],
    "tools":       [],
    "soft_skills": [],
}

def extract_keywords(job_description: str) -> dict:
    if not job_description.strip():
        return _EMPTY_KEYWORDS
    try:
        raw = _call(KEYWORD_PROMPT.format(job_description=job_description), max_tokens=1024)
        return _parse_json(raw)
    except Exception as e:
        print(f"[extract_keywords] failed: {e}")
        return _EMPTY_KEYWORDS


# ─────────────────────────────────────────────
# Public: resume analysis
# ─────────────────────────────────────────────

_EMPTY_ANALYSIS = {
    "target_role":        "",
    "ats_score":          0,
    "matched_keywords":   [],
    "missing_keywords":   [],
    "suggested_keywords": [],
    "section_feedback":   {},
    "bullet_quality":     "",
    "formatting_flags":   [],
    "suggestions":        [],
}

def analyse_resume(resume_text: str, job_description: str = "", keywords: list = []) -> dict:
    prompt = build_analyse_prompt(resume_text, job_description, keywords)
    try:
        raw    = _call(prompt, max_tokens=4096)
        result = _parse_json(raw)
        return result
    except Exception as e:
        print(f"[analyse_resume] failed: {e}")
        return _EMPTY_ANALYSIS