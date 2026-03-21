import json
import re
from typing import Dict, List

def extract_json(text:str) -> Dict:
    text = text.strip()

    text = re.sub(r"```json", "", text, flags = re.IGNORECASE).strip()
    text = re.sub(r"^```", "", text).strip()
    text = re.sub(r"```$", "", text).strip()

    try:
        return json.loads(text)
    except json.JSONDecodeError as e:
        # attempt to extract JSON object chunk if model adds extra text
        match = re.search(r"\{.*\}", text, re.DOTALL)
        if match:
            candidate = match.group(0)
            # remove trailing commas before closing braces
            candidate = re.sub(r",\s*([\}\]])", r"\1", candidate)
            try:
                return json.loads(candidate)
            except json.JSONDecodeError:
                # try replacing single quotes with double quotes (best-effort)
                candidate2 = candidate.replace("'", '"')
                try:
                    return json.loads(candidate2)
                except json.JSONDecodeError:
                    raise ValueError(f"Could Not Parse JSON from Model Response; last error: {e.msg} at line {e.lineno} col {e.colno}. content=\n{candidate[:1000]}")
        raise ValueError(f"Could Not Parse JSON from Model Response; last error: {e.msg} at line {e.lineno} col {e.colno}. full content=\n{text[:1000]}")
    
def clean_lines(text:str) -> List[str]:
    return [line.rstrip() for line in text.splitlines()]

def split_sections(text: str) -> Dict[str, List[str]]:
    section_map = {
        "professional_summary" : "Professional Summary",
        "summary" : "Professional Summary",
        "skills" : "Skills",
        "technical skills" : "Skills",
        "experience" : "Experience",
        "work experience" : "Experience",
        "projects" : "Projects",
        "education" : "Education"
    }

    sections = {
        "Professional Summary" : [],
        "Skills" : [],
        "Experience" : [],
        "Projects" : [],
        "Education" : [],
        "Other" : []
    }

    current = "Other"
    
    for raw_line in clean_lines(text):
        line = raw_line.strip()
        normalized = re.sub(r"[^a-z]", "", line.lower()).strip()

        if normalized in section_map:
            current = section_map[normalized]
            continue

        if line:
            sections[current].append(line)
    
    return sections