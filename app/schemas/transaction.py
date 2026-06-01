from pydantic import BaseModel, Field, field_validator
from typing import Optional
from datetime import datetime
from app.models.transaction import TransactionStatus, Currency


class TransactionCreate(BaseModel):
    amount: float = Field(..., gt=0, description="Amount must be greater than 0")
    currency: Currency
    merchant_name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = Field(default="", max_length=500)

    @field_validator("amount")
    @classmethod
    def round_amount(cls, v):
        return round(v, 2)


class TransactionStatusUpdate(BaseModel):
    status: TransactionStatus


class TransactionResponse(BaseModel):
    id: str
    amount: float
    currency: Currency
    merchant_name: str
    description: str
    status: TransactionStatus
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class PaginatedTransactionResponse(BaseModel):
    total: int
    page: int
    page_size: int
    results: list[TransactionResponse]