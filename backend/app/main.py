from __future__ import annotations

import math
from typing import Literal

import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

app = FastAPI(
    title="Heart Disease Prediction API",
    version="1.0.0",
    description="Educational heart disease risk assessment API. It is not a medical diagnosis.",
)

raw_origins = os.getenv("CORS_ORIGINS", "*")
origins = [item.strip() for item in raw_origins.split(",") if item.strip()]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins if origins else ["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

class AssessmentInput(BaseModel):
    age: int = Field(ge=18, le=120)
    sex: Literal[0, 1]  # 0 = female, 1 = male (UCI Heart Disease encoding)
    cp: Literal[0, 1, 2, 3]
    trestbps: int = Field(ge=70, le=260)
    chol: int = Field(ge=80, le=700)
    fbs: Literal[0, 1]
    restecg: Literal[0, 1, 2]
    thalach: int = Field(ge=40, le=240)
    exang: Literal[0, 1]
    oldpeak: float = Field(ge=0, le=10)
    slope: Literal[0, 1, 2]
    ca: Literal[0, 1, 2, 3, 4]
    thal: Literal[0, 1, 2, 3]


class AssessmentResponse(BaseModel):
    prediction: Literal[0, 1]
    risk_level: Literal["Low", "Moderate", "High"]
    probability: float
    message: str
    disclaimer: str


def _sigmoid(value: float) -> float:
    return 1 / (1 + math.exp(-max(min(value, 30), -30)))


def calculate_risk(patient: AssessmentInput) -> float:
    """Return a transparent educational risk estimate.

    Coefficients encode directional relationships commonly used in introductory
    UCI-heart-disease demonstrations. Replace this function with a validated,
    versioned clinical model before any real-world medical use.
    """
    score = -5.25
    score += 0.055 * (patient.age - 45)
    score += 0.42 * patient.sex
    score += [0.0, 0.28, 0.7, 1.18][patient.cp]
    score += 0.016 * max(patient.trestbps - 120, 0)
    score += 0.006 * max(patient.chol - 200, 0)
    score += 0.32 * patient.fbs
    score += 0.20 * patient.restecg
    score += 0.028 * max(150 - patient.thalach, 0)
    score += 0.88 * patient.exang
    score += 0.42 * patient.oldpeak
    score += [0.0, 0.30, 0.62][patient.slope]
    score += 0.48 * patient.ca
    score += [0.0, 0.20, 0.56, 0.78][patient.thal]
    return _sigmoid(score)


@app.get("/api/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/api/predict", response_model=AssessmentResponse)
def predict(patient: AssessmentInput) -> AssessmentResponse:
    probability = calculate_risk(patient)
    percentage = round(probability * 100, 1)
    if probability < 0.30:
        level: Literal["Low", "Moderate", "High"] = "Low"
        message = "The educational estimate is in the lower-risk range. Continue routine preventive care."
    elif probability < 0.60:
        level = "Moderate"
        message = "The educational estimate is in the moderate-risk range. Discuss your results with a clinician."
    else:
        level = "High"
        message = "The educational estimate is in the higher-risk range. Please seek advice from a qualified clinician."

    return AssessmentResponse(
        prediction=int(probability >= 0.50),
        risk_level=level,
        probability=percentage,
        message=message,
        disclaimer="For education only. This tool is not a diagnosis and must not guide emergency or treatment decisions.",
    )
