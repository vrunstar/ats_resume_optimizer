import streamlit as st

from src.extractor import extract_keywords
from src.optimizer import optimize_resume
from src.formatter import format_resume_text
from src.pdf_exporter import resume_to_pdf

st.set_page_config(page_title="AI based ATS Resume Optimizer",
                   layout="wide")
st.title("AI based ATS Resume Optimizer")
st.write("Paste the job description and your resume text. The app will optimize the resume for ATS and let you download it as a PDF.")

left, right = st.columns(2)

with left:
    job_description = st.text_area("Job Description", height=320)
with right:
    resume_text = st.text_area("Resume Text", height=320)

if st.button("Optimize Resume"):
    if not job_description.strip() or not resume_text.strip():
        st.warning("Please fill in both fields.")
    else:
        try:
            with st.spinner("Extracting Keywords..."):
                keyword_data = extract_keywords(job_description)
            
            keywords = keyword_data.get("keywords", [])

            with st.spinner("Optimizing Resume..."):
                result = optimize_resume(job_description, resume_text, keywords)
            
            optimized_resume = format_resume_text(
                result.get("optimized_resume") or result.get("optimized_resume") or result.get("optimized resume") or ""
            )

            st.subheader("Target Role")
            st.write(keyword_data.get("target_role", "Not Found"))

            st.subheader("Extracted Keywords")
            st.write(", ".join(keywords) if keywords else "No Keywords Extracted")

            st.subheader("ATS Optimized Resume")
            st.text_area("Output Resume", optimized_resume, height=500)

            st.subheader("Matched Keywords")
            matched = result.get("matched_keywords") or result.get("matched_keywords") or []
            st.write(", ".join(matched) if matched else "None")

            st.subheader("Missing Keywords")
            missing = result.get("missing_keywords") or result.get("missing_keywords") or []
            st.write(", ".join(missing) if missing else "None")

            st.subheader("Suggestions")
            suggestion = result.get("suggestions", [])
            if suggestion:
                for item in suggestion:
                    st.write(f"- {item}")
            else:
                st.write("No Suggestions")

            pdf_bytes = resume_to_pdf(optimized_resume)

            st.download_button(
                label="Download Resume as PDF",
                data=pdf_bytes,
                file_name="ats_optimized_resume.pdf",
                mime="application/pdf",
            )
        except Exception as e:
            st.error(f"Error : {e}")