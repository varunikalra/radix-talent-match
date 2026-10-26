from __future__ import annotations

from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from backend.jd_parser import (
    analysis_to_dict,
    analyze_job_description,
)

VERSION = "0.2.0"
PROJECT_ROOT = Path(__file__).resolve().parent.parent
SAMPLE_JD_DIRECTORY = PROJECT_ROOT / "data" / "sample_jds"

app = FastAPI(
    title="RADIX Talent Match API",
    description="Candidate-readiness and JD analytics API",
    version=VERSION,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:5174",
        "http://127.0.0.1:5174",
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)


class AnalyzeJDRequest(BaseModel):
    text: str = Field(..., min_length=1, description="Raw job description text")


class SampleJD(BaseModel):
    id: str
    name: str


class HealthResponse(BaseModel):
    status: str
    service: str
    version: str


class SampleJDText(BaseModel):
    id: str
    name: str
    text: str


@app.get("/api/health", response_model=HealthResponse)
def health() -> HealthResponse:
    return HealthResponse(
        status="ok",
        service="radix-talent-match-api",
        version=VERSION,
    )


@app.get("/api/jd-analytics/samples", response_model=list[SampleJD])
def list_sample_jobs() -> list[SampleJD]:
    return [
        SampleJD(id=path.stem, name=path.stem.replace("_", " ").title())
        for path in sorted(SAMPLE_JD_DIRECTORY.glob("*.txt"))
    ]


def _load_sample(path_id: str) -> tuple[Path, str]:
    if not path_id or Path(path_id).name != path_id:
        raise HTTPException(status_code=400, detail="A valid sample identifier is required.")

    path = SAMPLE_JD_DIRECTORY / f"{path_id}.txt"
    if not path.is_file():
        raise HTTPException(status_code=404, detail="The requested sample job description was not found.")

    try:
        return path, path.read_text(encoding="utf-8")
    except OSError as error:
        raise HTTPException(status_code=500, detail="The sample job description could not be read.") from error


@app.get("/api/jd-analytics/samples/{sample_id}", response_model=SampleJDText)
def get_sample_job(sample_id: str) -> SampleJDText:
    path, text = _load_sample(sample_id)
    return SampleJDText(
        id=path.stem,
        name=path.stem.replace("_", " ").title(),
        text=text,
    )


@app.post("/api/jd-analytics/analyze")
def analyze_job( request: AnalyzeJDRequest) -> dict:
    text = request.text.strip()
    if not text:
        raise HTTPException(status_code=422, detail="Job description text cannot be empty.")

    return analysis_to_dict(analyze_job_description(text))
