from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from models import EvaluateRequest, Evaluation
from problems import PROBLEMS, get_problem
from executor import run_python
from evaluator import evaluate


app = FastAPI(title="TalentAI — Code Evaluation Prototype")

# Open CORS for local dev. Lock this down before integrating with TalentAI.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/problems")
def list_problems():
    return [{"id": p["id"], "title": p["title"]} for p in PROBLEMS.values()]


@app.get("/problems/{problem_id}")
def problem_detail(problem_id: str):
    p = get_problem(problem_id)
    if not p:
        raise HTTPException(404, "Unknown problem")
    return {k: p[k] for k in ("id", "title", "description", "function_name", "starter_code")}


@app.post("/evaluate", response_model=Evaluation)
def evaluate_submission(req: EvaluateRequest):
    p = get_problem(req.problem_id)
    if not p:
        raise HTTPException(404, "Unknown problem")
    if req.language != "python":
        raise HTTPException(400, "Prototype supports Python only")

    # 1. Ground truth: run the code against real test cases.
    test_results = run_python(req.code, p["function_name"], p["test_cases"])
    # 2. HR-facing verdict: Gemini translates results + code into a recommendation.
    return evaluate(p, req.code, test_results)
