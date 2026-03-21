def format_resume_text(resume_text: str) -> str:
    lines = [line.rstrip() for line in resume_text.splitlines()]
    cleaned = []

    for line in lines:
        if line.strip():
            cleaned.append(line.strip())
        else:
            cleaned.append("")

    return "\n".join(cleaned).strip()