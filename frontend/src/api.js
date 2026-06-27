import axios from "axios";

const BASE_URL = import.meta.env.VITE_API_URL || "";

export async function analyseResume({ resumeFile, resumeText, jobDescription }) {
  const form = new FormData();

  if (resumeFile) {
    form.append("resume_file", resumeFile);
  } else {
    form.append("resume_text", resumeText || "");
  }

  form.append("job_description", jobDescription || "");

  const { data } = await axios.post(`${BASE_URL}/analyse`, form, {
    headers: { "Content-Type": "multipart/form-data" },
  });

  return data;
}