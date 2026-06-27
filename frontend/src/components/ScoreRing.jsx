import { useEffect, useState } from "react";

function getColor(score) {
  if (score >= 75) return "var(--green)";
  if (score >= 50) return "var(--yellow)";
  return "var(--red)";
}

function getLabel(score) {
  if (score >= 75) return "Strong";
  if (score >= 50) return "Fair";
  return "Weak";
}

export default function ScoreRing({ score = 0, size = 160 }) {
  const [displayed, setDisplayed] = useState(0);

  const radius      = (size - 16) / 2;
  const circumference = 2 * Math.PI * radius;
  const color       = getColor(displayed);
  const offset      = circumference - (displayed / 100) * circumference;

  // Animate score counting up on mount
  useEffect(() => {
    if (score === 0) return;
    let current = 0;
    const step  = Math.ceil(score / 40);
    const timer = setInterval(() => {
      current += step;
      if (current >= score) {
        setDisplayed(score);
        clearInterval(timer);
      } else {
        setDisplayed(current);
      }
    }, 20);
    return () => clearInterval(timer);
  }, [score]);

  return (
    <div
      style={{
        display:        "flex",
        flexDirection:  "column",
        alignItems:     "center",
        gap:            "8px",
      }}
    >
      <svg width={size} height={size} style={{ transform: "rotate(-90deg)" }}>
        {/* Track */}
        <circle
          cx={size / 2}
          cy={size / 2}
          r={radius}
          fill="none"
          stroke="var(--border)"
          strokeWidth={10}
        />
        {/* Progress */}
        <circle
          cx={size / 2}
          cy={size / 2}
          r={radius}
          fill="none"
          stroke={color}
          strokeWidth={10}
          strokeLinecap="round"
          strokeDasharray={circumference}
          strokeDashoffset={offset}
          style={{ transition: "stroke-dashoffset 0.05s linear, stroke 0.3s ease" }}
        />
        {/* Score text — counter-rotate so it reads upright */}
        <text
          x="50%"
          y="50%"
          dominantBaseline="middle"
          textAnchor="middle"
          style={{
            transform:      `rotate(90deg)`,
            transformOrigin: "center",
            fontSize:        size * .3,
            fontWeight:      800,
            fontFamily:      "var(--font-sans)",
            fill:            color,
          }}
        >
          {displayed}
        </text>
      </svg>

      <div style={{ textAlign: "center" }}>
        <div
          style={{
            fontSize:   "1rem",
            fontWeight: 600,
            color,
            letterSpacing: "0.05em",
            textTransform: "uppercase",
          }}
        >
          {getLabel(displayed)}
        </div>
        <div style={{ fontSize: "0.72rem", color: "var(--muted)", marginTop: "2px" }}>
          ATS Score
        </div>
      </div>
    </div>
  );
}