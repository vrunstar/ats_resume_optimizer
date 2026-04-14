# AI-based ATS Resume Optimizer

A Streamlit app that analyzes a job description and your resume, then generates an ATS-friendly optimized resume with keyword matching and PDF export.

## Features

- Extracts role, keywords, skills, tools, and soft skills from job description using AI model
- Rewrites resume text to align with job description (ATS-friendly)
- Highlights matched and missing keywords
- Provides suggestions
- Exports optimized resume to PDF (split into sections, bullet formatting)

## Project Structure

- `app.py` — Streamlit UI and orchestration
- `src/extractor.py` — runs keyword extraction prompt
- `src/optimizer.py` — runs resume optimization prompt
- `src/formatter.py` — normalize output text formatting
- `src/pdf_exporter.py` — converts optimized text to PDF using ReportLab
- `src/parser.py` — resilient JSON extraction from model response
- `src/gemini_client.py` — model client wrapper
- `src/prompt.py` — prompt templates
- `src/config.py` — environment configuration for Gemini API

## Prerequisites

- Python 3.11+
- `pip` package manager
- `streamlit` for running app
- `reportlab` for PDF generation
- Google Gemini API key and model configured in `src/config.py`

## Install dependencies

```bash
pip install -r requirements.txt
```

If `requirements.txt` is missing one or more packages, add manually:

```bash
pip install streamlit reportlab google-generativeai
```

## Configuration

Edit `src/config.py`:

```python
GEMINI_API_KEY = "YOUR_API_KEY"
GEMINI_MODEL = "gemini-2.5-flash"  # or whichever model you use
```

## Run locally

```bash
streamlit run app.py
```

Open the URL provided by Streamlit in your browser.

## Usage

1. Paste job description into left column.
2. Paste your current resume text into right column.
3. Click **Optimize Resume**.
4. Review:
   - Target Role
   - Extracted Keywords
   - ATS Optimized Resume
   - Matched/ Missing Keywords
   - Suggestions
5. Click **Download Resume as PDF**.

## Error handling and robust behavior

- `extract_json` in `src/parser.py` will:
  - strip code fences (```json)
  - fallback to first `{...}` JSON block
  - remove trailing commas `,}` / `,]`
  - optionally replace single quotes to double quotes
- `pdf_exporter` now uses `styles["BodyText"]` (valid ReportLab style)

## Common issues

- `Error: Style 'Bodytext' not found` -> fixed in `src/pdf_exporter.py`
- `Expecting ',' delimiter` -> invalid AI output JSON; the parser now handles extra formatting and reports snippet.
- Model call fails: check API key, model config, network connectivity.

## Testing

Static syntax check:

```bash
python -m py_compile app.py src/*.py
```

## Enhancement ideas

- Add a local `fallback` non-AI text rewrite path
- Add optional source/experience section mapping
- Use fine-tuned model for better resume-specific JSON output
- Add configurable output language, formatting style, and ATS scoring

## License

This project is licensed under MIT License.
