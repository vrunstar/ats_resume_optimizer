import { useState, useRef } from "react";
import { useNavigate } from "react-router-dom";
import { analyseResume } from "../api.js";

const styles = {
  page: {
    minHeight:     "100vh",
    background:    "var(--bg)",
    display:       "flex",
    flexDirection: "column",
  },
  header: {
    borderBottom: "1px solid var(--border)",
    padding:      "20px 40px",
    display:      "flex",
    alignItems:   "center",
    gap:          "10px",
  },
  logo: {
    fontFamily: "var(--font-serif)",
    fontSize:   "1.75rem",
    color:      "var(--text)",
    letterSpacing: "-0.01em",
  },
  logoAccent: {
    color: "var(--accent)",
  },
  main: {
    flex:          1,
    maxWidth:      "860px",
    margin:        "0 auto",
    padding:       "60px 24px 80px",
    width:         "100%",
  },
  hero: {
    textAlign:    "center",
    marginBottom: "48px",
  },
  heroTitle: {
    fontFamily:  "var(--font-serif)",
    fontSize:    "clamp(2rem, 5vw, 2.8rem)",
    color:       "var(--text)",
    lineHeight:  1.15,
    marginBottom:"12px",
  },
  heroSub: {
    fontSize:  "1rem",
    color:     "var(--muted)",
    maxWidth:  "760px",
    margin:    "0 auto",
    lineHeight: 1.6,
  },
  card: {
    background:   "var(--bg)",
    border:       "1px solid var(--border)",
    borderRadius: "12px",
    padding:      "32px",
    marginBottom: "20px",
  },
  label: {
    display:      "block",
    fontSize:     "0.82rem",
    fontWeight:   600,
    color:        "var(--text)",
    marginBottom: "8px",
    letterSpacing:"0.02em",
    textTransform:"uppercase",
  },
  dropzone: {
    border:        "2px dashed var(--border)",
    borderRadius:  "var(--radius)",
    padding:       "36px 24px",
    textAlign:     "center",
    cursor:        "pointer",
    transition:    "border-color 0.2s, background 0.2s",
    background:    "var(--surface)",
  },
  dropzoneActive: {
    borderColor: "var(--accent)",
    background:  "var(--accent-lt)",
  },
  dropIcon: {
    fontSize:     "2rem",
    marginBottom: "8px",
  },
  dropText: {
    fontSize:  "0.9rem",
    color:     "var(--muted)",
    lineHeight: 1.5,
  },
  dropBrowse: {
    color:      "var(--accent)",
    fontWeight: 600,
    cursor:     "pointer",
  },
  fileChip: {
    display:      "inline-flex",
    alignItems:   "center",
    gap:          "8px",
    padding:      "6px 12px",
    background:   "var(--accent-lt)",
    border:       "1px solid #bfdbfe",
    borderRadius: "var(--radius)",
    fontSize:     "0.85rem",
    color:        "var(--accent)",
    fontWeight:   500,
    marginTop:    "12px",
  },
  removeBtn: {
    background: "none",
    border:     "none",
    color:      "var(--accent)",
    cursor:     "pointer",
    fontSize:   "1rem",
    lineHeight: 1,
    padding:    0,
  },
  divider: {
    display:    "flex",
    alignItems: "center",
    gap:        "12px",
    margin:     "8px 0",
    color:      "var(--muted)",
    fontSize:   "0.8rem",
  },
  dividerLine: {
    flex:       1,
    height:     "1px",
    background: "var(--border)",
  },
  textarea: {
    width:        "100%",
    minHeight:    "120px",
    padding:      "12px 14px",
    border:       "1px solid var(--border)",
    borderRadius: "var(--radius)",
    fontFamily:   "var(--font-sans)",
    fontSize:     "0.9rem",
    color:        "var(--text)",
    background:   "var(--surface)",
    resize:       "vertical",
    outline:      "none",
    lineHeight:   1.6,
    transition:   "border-color 0.2s",
  },
  optional: {
    fontSize:   "0.75rem",
    color:      "var(--muted)",
    fontWeight: 400,
    marginLeft: "6px",
    textTransform: "none",
    letterSpacing: 0,
  },
  submitBtn: {
    width:        "100%",
    padding:      "14px",
    background:   "var(--accent)",
    color:        "#fff",
    border:       "none",
    borderRadius: "var(--radius)",
    fontSize:     "0.95rem",
    fontWeight:   600,
    cursor:       "pointer",
    fontFamily:   "var(--font-sans)",
    transition:   "opacity 0.2s",
    marginTop:    "8px",
  },
  error: {
    background:   "var(--red-lt)",
    border:       "1px solid #fecaca",
    borderRadius: "var(--radius)",
    padding:      "12px 16px",
    color:        "var(--red)",
    fontSize:     "0.875rem",
    marginTop:    "16px",
  },
  scanBar: {
    height:     "3px",
    background: "var(--border)",
    borderRadius: "999px",
    overflow:   "hidden",
    marginBottom: "32px",
  },
  scanFill: {
    height:     "100%",
    background: "var(--accent)",
    borderRadius: "999px",
    animation:  "scan 1.4s ease-in-out infinite",
  },
};

const scanKeyframes = `
@keyframes scan {
  0%   { width: 0%;   margin-left: 0%; }
  50%  { width: 60%;  margin-left: 20%; }
  100% { width: 0%;   margin-left: 100%; }
}
`;

export default function Home() {
  const navigate    = useNavigate();
  const fileInputRef = useRef(null);

  const [resumeFile,      setResumeFile]      = useState(null);
  const [resumeText,      setResumeText]      = useState("");
  const [jobDescription,  setJobDescription]  = useState("");
  const [dragging,        setDragging]        = useState(false);
  const [loading,         setLoading]         = useState(false);
  const [error,           setError]           = useState("");

  function handleFile(file) {
    if (!file) return;
    const ext = file.name.split(".").pop().toLowerCase();
    if (!["pdf", "docx"].includes(ext)) {
      setError("Only PDF and DOCX files are supported.");
      return;
    }
    setError("");
    setResumeFile(file);
    setResumeText("");
  }

  function onDrop(e) {
    e.preventDefault();
    setDragging(false);
    handleFile(e.dataTransfer.files[0]);
  }

  async function handleSubmit() {
    if (!resumeFile && !resumeText.trim()) {
      setError("Please upload a resume or paste your resume text.");
      return;
    }
    setError("");
    setLoading(true);
    try {
      const result = await analyseResume({ resumeFile, resumeText, jobDescription });
      navigate("/results", { state: { result, jobDescription } });
    } catch (err) {
      const msg = err.response?.data?.detail || err.message || "Something went wrong.";
      setError(msg);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div style={styles.page}>
      <style>{scanKeyframes}</style>

      {/* Header */}
      <header style={styles.header}>
        <div style={{ display: "flex", alignItems: "center", gap: "10px" }}>
          <div style={styles.logo}>
            ATS <span style={styles.logoAccent}>Check</span>
          </div>
        </div>
      </header>

      <main style={styles.main}>
        {/* Hero */}
        <div style={styles.hero}>
          <h1 style={styles.heroTitle}>
            Is your resume ATS-ready?
          </h1>
          <p style={styles.heroSub}>
            Upload your resume and optionally paste a job description.
            </p>
            <p style={styles.heroSub}>
            Get an instant report card — score, keyword gaps, and actionable fixes.
          </p>
        </div>

        {/* Scanning bar — shown while loading */}
        {loading && (
          <div style={styles.scanBar}>
            <div style={styles.scanFill} />
          </div>
        )}

        {/* Resume upload card */}
        <div style={styles.card}>
          <label style={styles.label}>Your Resume</label>

          {/* Dropzone */}
          <div
            style={{ ...styles.dropzone, ...(dragging ? styles.dropzoneActive : {}) }}
            onClick={() => fileInputRef.current?.click()}
            onDragOver={(e) => { e.preventDefault(); setDragging(true); }}
            onDragLeave={() => setDragging(false)}
            onDrop={onDrop}
          >
            <div style={styles.dropIcon}>📄</div>
            <div style={styles.dropText}>
              Drag & drop your resume here, or{" "}
              <span style={styles.dropBrowse}>browse</span>
              <br />
              <span style={{ fontSize: "0.78rem" }}>PDF or DOCX · Max 5MB</span>
            </div>
            <input
              ref={fileInputRef}
              type="file"
              accept=".pdf,.docx"
              style={{ display: "none" }}
              onChange={(e) => handleFile(e.target.files[0])}
            />
          </div>

          {/* File chip */}
          {resumeFile && (
            <div style={styles.fileChip}>
              📎 {resumeFile.name}
              <button
                style={styles.removeBtn}
                onClick={(e) => { e.stopPropagation(); setResumeFile(null); }}
              >
                ×
              </button>
            </div>
          )}

          {/* OR divider + paste option */}
          {!resumeFile && (
            <>
              <div style={styles.divider}>
                <span style={styles.dividerLine} />
                or paste text
                <span style={styles.dividerLine} />
              </div>
              <textarea
                style={styles.textarea}
                placeholder="Paste your resume text here…"
                value={resumeText}
                onChange={(e) => setResumeText(e.target.value)}
                onFocus={(e)  => (e.target.style.borderColor = "var(--accent)")}
                onBlur={(e)   => (e.target.style.borderColor = "var(--border)")}
              />
            </>
          )}
        </div>

        {/* Job description card */}
        <div style={styles.card}>
          <label style={styles.label}>
            Job Description
            <span style={styles.optional}>optional</span>
          </label>
          <textarea
            style={{ ...styles.textarea, minHeight: "160px" }}
            placeholder="Paste the job description here for a role-specific analysis…"
            value={jobDescription}
            onChange={(e) => setJobDescription(e.target.value)}
            onFocus={(e)  => (e.target.style.borderColor = "var(--accent)")}
            onBlur={(e)   => (e.target.style.borderColor = "var(--border)")}
          />
        </div>

        {/* Error */}
        {error && <div style={styles.error}>{error}</div>}

        {/* Submit */}
        <button
          style={{ ...styles.submitBtn, opacity: loading ? 0.7 : 1 }}
          onClick={handleSubmit}
          disabled={loading}
        >
          {loading ? "Analysing…" : "Check My Resume →"}
        </button>
      </main>
    </div>
  );
}