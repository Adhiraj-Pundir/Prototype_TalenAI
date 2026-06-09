import { useEffect, useState } from "react";
import Editor from "@monaco-editor/react";

const API = "http://localhost:8001";
const PROBLEM_ID = "two-sum";

const C = {
  bg: "#0d1117",
  panel: "#161b22",
  border: "#30363d",
  text: "#e6edf3",
  muted: "#8b949e",
  accent: "#58a6ff",
  pass: "#3fb950",
  fail: "#f85149",
  warn: "#d29922",
};

export default function App() {
  const [problem, setProblem] = useState(null);
  const [code, setCode] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetch(`${API}/problems/${PROBLEM_ID}`)
      .then((r) => r.json())
      .then((p) => {
        setProblem(p);
        setCode(p.starter_code);
      })
      .catch(() => setError("Backend not reachable. Is FastAPI running on :8000?"));
  }, []);

  async function evaluate() {
    setLoading(true);
    setError(null);
    setResult(null);
    try {
      const res = await fetch(`${API}/evaluate`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ problem_id: PROBLEM_ID, language: "python", code }),
      });
      if (!res.ok) throw new Error((await res.json()).detail || "Request failed");
      setResult(await res.json());
    } catch (e) {
      setError(e.message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div style={{ display: "flex", height: "100vh", background: C.bg, color: C.text,
      fontFamily: "system-ui, -apple-system, sans-serif" }}>

      {/* LEFT: problem */}
      <div style={{ width: "34%", padding: 24, overflowY: "auto", borderRight: `1px solid ${C.border}` }}>
        <div style={{ fontSize: 12, color: C.accent, letterSpacing: 1, textTransform: "uppercase" }}>
          TalentAI · Technical Screen
        </div>
        <h1 style={{ fontSize: 22, margin: "8px 0 16px" }}>{problem?.title ?? "Loading…"}</h1>
        <pre style={{ whiteSpace: "pre-wrap", color: C.muted, lineHeight: 1.6, fontSize: 14,
          fontFamily: "inherit" }}>
          {problem?.description}
        </pre>
      </div>

      {/* RIGHT: editor + results */}
      <div style={{ flex: 1, display: "flex", flexDirection: "column" }}>
        <div style={{ flex: 1, minHeight: 0 }}>
          <Editor
            height="100%"
            language="python"
            theme="vs-dark"
            value={code}
            onChange={(v) => setCode(v ?? "")}
            options={{ fontSize: 14, minimap: { enabled: false }, scrollBeyondLastLine: false }}
          />
        </div>

        <div style={{ padding: "12px 16px", borderTop: `1px solid ${C.border}`,
          display: "flex", alignItems: "center", gap: 12 }}>
          <button
            onClick={evaluate}
            disabled={loading || !problem}
            style={{ background: C.accent, color: "#0d1117", border: "none", borderRadius: 6,
              padding: "8px 18px", fontWeight: 600, cursor: loading ? "wait" : "pointer" }}>
            {loading ? "Evaluating…" : "Submit for evaluation"}
          </button>
          {error && <span style={{ color: C.fail, fontSize: 13 }}>{error}</span>}
        </div>

        {result && (
          <div style={{ maxHeight: "45%", overflowY: "auto", padding: 16,
            borderTop: `1px solid ${C.border}`, background: C.panel }}>
            <Verdict r={result} />
          </div>
        )}
      </div>
    </div>
  );
}

function Verdict({ r }) {
  const pass = r.recommendation === "pass";
  const color = pass ? C.pass : C.fail;
  const confColor = { high: C.pass, medium: C.warn, low: C.fail }[r.confidence] ?? C.muted;

  return (
    <div style={{ fontSize: 14 }}>
      <div style={{ display: "flex", alignItems: "center", gap: 12, marginBottom: 6 }}>
        <span style={{ fontSize: 11, color: C.muted, textTransform: "uppercase", letterSpacing: 1 }}>
          Recommendation
        </span>
        <span style={{ color, fontWeight: 700, fontSize: 16 }}>
          {pass ? "Recommend pass" : "Recommend no-pass"}
        </span>
        <span style={{ color: confColor, fontSize: 12, border: `1px solid ${confColor}`,
          borderRadius: 4, padding: "1px 6px" }}>
          {r.confidence} confidence
        </span>
      </div>

      <p style={{ margin: "0 0 14px", lineHeight: 1.6 }}>{r.summary}</p>

      <div style={{ display: "grid", gap: 8, marginBottom: 14 }}>
        <Row label="Tests passed" value={r.evidence.tests_passed} />
        <Row label="What worked" value={r.evidence.what_worked} />
        <Row label="What failed" value={r.evidence.what_failed} />
        <Row label="Concerns" value={r.evidence.concerns} />
      </div>

      <div style={{ fontSize: 11, color: C.muted, marginBottom: 8 }}>
        TEST DETAIL
      </div>
      {r.test_results.map((t, i) => (
        <div key={i} style={{ display: "flex", gap: 10, fontSize: 13, padding: "3px 0",
          fontFamily: "ui-monospace, monospace" }}>
          <span style={{ color: t.passed ? C.pass : C.fail, width: 16 }}>{t.passed ? "✓" : "✗"}</span>
          <span style={{ width: 110, color: C.muted }}>{t.name}</span>
          <span style={{ color: C.muted }}>
            {t.error ? `error: ${t.error}` : `got ${t.got} · want ${t.expected}`}
          </span>
        </div>
      ))}
    </div>
  );
}

function Row({ label, value }) {
  return (
    <div style={{ display: "flex", gap: 12 }}>
      <span style={{ width: 110, color: C.muted, fontSize: 12, flexShrink: 0 }}>{label}</span>
      <span style={{ lineHeight: 1.5 }}>{value}</span>
    </div>
  );
}
