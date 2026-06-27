import io


def read_pdf(file_bytes: bytes) -> str:
    """Extract text from a PDF file using pdfplumber."""
    import pdfplumber

    pages = []
    with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                pages.append(text)
    return "\n".join(pages)


def read_docx(file_bytes: bytes) -> str:
    """Extract text from a DOCX file using python-docx."""
    from docx import Document

    doc = Document(io.BytesIO(file_bytes))
    lines = [p.text for p in doc.paragraphs if p.text.strip()]
    return "\n".join(lines)


def extract_resume_text(filename: str, file_bytes: bytes) -> str:
    """
    Dispatch to the correct extractor based on file extension.
    Raises ValueError for unsupported types.
    """
    fname = filename.lower()
    if fname.endswith(".pdf"):
        return read_pdf(file_bytes)
    elif fname.endswith(".docx"):
        return read_docx(file_bytes)
    else:
        raise ValueError(f"Unsupported file type: '{filename}'. Please upload a PDF or DOCX.")