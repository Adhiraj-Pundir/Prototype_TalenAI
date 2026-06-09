from pydantic import BaseModel
from typing import Literal, Optional, List


class EvaluateRequest(BaseModel):
    problem_id: str
    language: str
    code: str


class TestResult(BaseModel):
    name: str
    passed: bool
    expected: str
    got: Optional[str] = None
    error: Optional[str] = None


class Evidence(BaseModel):
    tests_passed: str
    what_worked: str
    what_failed: str
    concerns: str


class Evaluation(BaseModel):
    recommendation: Literal["pass", "no_pass"]
    confidence: Literal["high", "medium", "low"]
    summary: str
    evidence: Evidence
    hr_action_required: bool = True
    test_results: List[TestResult]
