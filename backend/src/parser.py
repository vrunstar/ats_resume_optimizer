import json
import re
from typing import Dict, List


def extract_json(text: str) -> Dict:
    text = text.strip()
    text = re.sub(r"```json", "", text, flags=re.IGNORECASE).strip()
    text = re.sub(r"^```", "", text).strip()
    text = re.sub(r"```$", "", text).strip()

    try:
        return json.loads(text)
    except json.JSONDecodeError as e:
        match = re.search(r"\{.*\}", text, re.DOTALL)
        if match:
            candidate = match.group(0)
            candidate = re.sub(r",\s*([\}\]])", r"\1", candidate)
            try:
                return json.loads(candidate)
            except json.JSONDecodeError:
                candidate2 = candidate.replace("'", '"')
                try:
                    return json.loads(candidate2)
                except json.JSONDecodeError:
                    raise ValueError(
                        f"Could not parse JSON from model response. "
                        f"Error: {e.msg} at line {e.lineno} col {e.colno}.\n"
                        f"Content:\n{candidate[:1000]}"
                    )
        raise ValueError(
            f"Could not parse JSON from model response. "
            f"Error: {e.msg} at line {e.lineno} col {e.colno}.\n"
            f"Full content:\n{text[:1000]}"
        )


def clean_lines(text: str) -> List[str]:
    return [line.rstrip() for line in text.splitlines()]


def split_sections(text: str) -> Dict[str, List[str]]:
    section_map = {
        "professional summary": "Professional Summary",
        "summary":              "Professional Summary",
        "skills":               "Skills",
        "technical skills":     "Skills",
        "experience":           "Experience",
        "work experience":      "Experience",
        "projects":             "Projects",
        "education":            "Education",
    }

    sections: Dict[str, List[str]] = {
        "Professional Summary": [],
        "Skills":               [],
        "Experience":           [],
        "Projects":             [],
        "Education":            [],
        "Other":                [],
    }

    current = "Other"

    for raw_line in clean_lines(text):
        normalized = re.sub(r"\s+", " ", raw_line.lower()).strip()
        normalized = re.sub(r"[:\-]+$", "", normalized).strip()

        if normalized in section_map:
            current = section_map[normalized]
            continue

        if raw_line.strip():
            sections[current].append(raw_line.strip())

    return sections