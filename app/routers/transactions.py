from fastapi import APIRouter, Query
from typing import Optional
from app.schemas.transaction import (
    TransactionCreate,
    TransactionResponse,
    TransactionStatusUpdate,
    PaginatedTransactionResponse,
)
from app.models.transaction import TransactionStatus, Currency
from app.services.transaction_service import transaction_service

router = APIRouter(prefix="/transactions", tags=["Transactions"])


@router.post("/", response_model=TransactionResponse, status_code=201)
async def create_transaction(data: TransactionCreate):
    transaction = transaction_service.create_transaction(data)
    return transaction.to_dict()


@router.get("/", response_model=PaginatedTransactionResponse)
async def get_all_transactions(
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=10, ge=1, le=100),
    status: Optional[TransactionStatus] = None,
    currency: Optional[Currency] = None,
):
    return transaction_service.get_all_transactions(
        page=page,
        page_size=page_size,
        status=status,
        currency=currency,
    )


@router.get("/{transaction_id}", response_model=TransactionResponse)
async def get_transaction(transaction_id: str):
    transaction = transaction_service.get_transaction(transaction_id)
    return transaction.to_dict()


@router.patch("/{transaction_id}/status", response_model=TransactionResponse)
async def update_transaction_status(
    transaction_id: str, data: TransactionStatusUpdate
):
    transaction = transaction_service.update_status(
        transaction_id, data.status
    )
    return transaction.to_dict()


@router.delete("/{transaction_id}", status_code=200)
async def delete_transaction(transaction_id: str):
    return transaction_service.delete_transaction(transaction_id)