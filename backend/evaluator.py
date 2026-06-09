"""
Gemini layer. Its job is NOT to decide correctness — the test harness already
did that. Its job is to translate raw results + code quality into a plain-English
recommendation a non-technical HR reviewer can act on.

It RECOMMENDS. A human DECIDES. hr_action_required is always True.
"""

import os
import json
import requests
from dotenv import load_dotenv

load_dotenv()

# We support either OPENROUTER_API_KEY or GEMINI_API_KEY
API_KEY = os.environ.get("OPENROUTER_API_KEY") or os.environ.get("GEMINI_API_KEY")
MODEL = os.environ.get("OPENROUTER_MODEL", "openrouter/free")


def _build_prompt(problem, code, test_results):
    passed = sum(1 for t in test_results if t["passed"])
    total = len(test_results)
    return f"""You are evaluating a candidate's code submission for a hiring technical screen.
Your output is read by a NON-TECHNICAL HR reviewer. Use plain English. No jargon
like "O(n^2)" or "cyclomatic complexity" unless you immediately explain it simply.

PROBLEM: {problem['title']}
{problem['description']}

CANDIDATE CODE:
```python
{code}
```

TEST RESULTS (ground truth — trust these for correctness): {passed}/{total} passed
{json.dumps(test_results, indent=2)}

Return ONLY valid JSON. No markdown, no backticks, no prose before or after.
Exact structure:
{{
  "recommendation": "pass" or "no_pass",
  "confidence": "high" or "medium" or "low",
  "summary": "one HR-readable sentence on whether they cleared the bar and why",
  "evidence": {{
    "tests_passed": "{passed}/{total}",
    "what_worked": "plain English — what the candidate did well",
    "what_failed": "plain English — what broke, or 'Nothing significant'",
    "concerns": "approach/readability/edge-case issues, or 'None'"
  }}
}}

Rules:
- Correctness comes from the test results, not your own judgment of the code.
  If most tests fail, you should lean "no_pass".
- Beyond pass/fail, judge approach, readability, and edge-case handling —
  the things tests can't measure.
- Lower your "confidence" when results are borderline or the code is unusual.
- You are NOT making the hiring decision. You recommend; a human decides."""


def evaluate(problem, code, test_results):
    prompt = _build_prompt(problem, code, test_results)
    
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "http://localhost:5173",
        "X-Title": "TalentAI Code Evaluation Prototype"
    }
    
    payload = {
        "model": MODEL,
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }
    
    text = ""
    try:
        resp = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            json=payload,
            timeout=30
        )
        resp.raise_for_status()
        resp_data = resp.json()
        if "choices" in resp_data and len(resp_data["choices"]) > 0:
            text = resp_data["choices"][0]["message"]["content"].strip()
    except Exception as e:
        print(f"OpenRouter API call failed: {e}")
        text = ""

    if text.startswith("```"):
        text = text.strip("`")
        if text.lstrip().lower().startswith("json"):
            text = text.lstrip()[4:]
    text = text.strip()

    try:
        data = json.loads(text)
    except json.JSONDecodeError:
        # Defensive fallback so the endpoint never 500s on a malformed LLM reply.
        passed = sum(1 for t in test_results if t["passed"])
        total = len(test_results)
        data = {
            "recommendation": "pass" if passed == total else "no_pass",
            "confidence": "low",
            "summary": "Automated summary unavailable — review the raw results below.",
            "evidence": {
                "tests_passed": f"{passed}/{total}",
                "what_worked": "See test results.",
                "what_failed": "See test results.",
                "concerns": "LLM summary failed to parse; manual review needed.",
            },
        }

    data["hr_action_required"] = True
    data["test_results"] = test_results
    return data
