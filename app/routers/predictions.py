from fastapi import APIRouter
from pydantic import BaseModel, Field
from typing import Optional
from ml.model import fraud_model, FraudPrediction

router = APIRouter(prefix="/predictions", tags=["Fraud Detection"])


class PredictionRequest(BaseModel):
    amount: float = Field(..., gt=0)
    hour_of_day: int = Field(..., ge=0, le=23)
    is_international: bool = False
    transaction_count_24h: int = Field(..., ge=0)
    avg_transaction_amount: float = Field(..., gt=0)
    merchant_name: Optional[str] = None


class PredictionResponse(BaseModel):
    risk_score: float
    is_fraud: bool
    risk_level: str
    explanation: dict
    merchant_name: Optional[str] = None


@router.post("/", response_model=PredictionResponse)
async def predict_fraud(request: PredictionRequest):
    features = {
        "amount": request.amount,
        "hour_of_day": request.hour_of_day,
        "is_international": int(request.is_international),
        "transaction_count_24h": request.transaction_count_24h,
        "avg_transaction_amount": request.avg_transaction_amount,
    }

    prediction = fraud_model.predict(features)

    if prediction.risk_score < 0.3:
        risk_level = "LOW"
    elif prediction.risk_score < 0.7:
        risk_level = "MEDIUM"
    else:
        risk_level = "HIGH"

    return PredictionResponse(
        risk_score=prediction.risk_score,
        is_fraud=prediction.is_fraud,
        risk_level=risk_level,
        explanation=prediction.explanation,
        merchant_name=request.merchant_name,
    )