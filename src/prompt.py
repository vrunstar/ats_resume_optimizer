KEYWORD_PROMPT = """
You are an ATS resume analyst

Given a job description, return valid JSON only with these keys:
- target_role : string
- keywords : list of strings
- skills : list of strings
- tools : list of strings
- soft_skills : list of strings

Rules:
- Keep keywords concise
- Prefer exact wording from the job description
- No explanation text
- Output valid JSON only

Job Description :
{job_description}
"""

OPTIMIZE_PROMPT = """
You are an expert ATS resume writer

task : 
Rewrite the resume so it is better aligned to the job description.
Use the keywords, skills, tools, and soft skills provided.

Hard Rules:
- Do not invent new information, expereinces, companies, projects, tools, certificates, dates or metrics. Only use the information provided in the resume and the job description.
- Keep all claims truthful and based only on the original resume content.
- use ATS-freindly formatting and wording.
- Naturally include relevant keywords only where supported.
- Make the resume clean, concise, and readable.
- Output must be in plain text.

Formatting Rules:
- For Expereince and Projects, use bullet points starting with "- " and keep each bullet point to one line.
- Keep section titles exactly as written above.
- Do not use tables, columns, icons, or special symbols.

Return valid JSON only with these keys:
- optimized_resume : string
- matched_keywords : list of strings
- missing_keywords : list of strings
- suggestions : list of strings

Job Description :
{job_description}

Extracted Keywords : 
{keywords}

Original Resume : 
{resume_text}
"""