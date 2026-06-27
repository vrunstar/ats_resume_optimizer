const VARIANTS = {
  matched: {
    bg:     "var(--green-lt)",
    color:  "var(--green)",
    border: "#bbf7d0",
    label:  "✓",
  },
  missing: {
    bg:     "var(--red-lt)",
    color:  "var(--red)",
    border: "#fecaca",
    label:  "✗",
  },
  suggested: {
    bg:     "var(--yellow-lt)",
    color:  "var(--yellow)",
    border: "#fde68a",
    label:  "+",
  },
};

export default function KeywordBadge({ word, variant = "matched" }) {
  const v = VARIANTS[variant] || VARIANTS.matched;

  return (
    <span
      style={{
        display:       "inline-flex",
        alignItems:    "center",
        gap:           "4px",
        padding:       "3px 10px",
        borderRadius:  "999px",
        fontSize:      "0.78rem",
        fontWeight:    500,
        background:    v.bg,
        color:         v.color,
        border:        `1px solid ${v.border}`,
        whiteSpace:    "nowrap",
      }}
    >
      <span style={{ fontWeight: 700 }}>{v.label}</span>
      {word}
    </span>
  );
}