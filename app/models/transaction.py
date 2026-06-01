from enum import Enum
from datetime import datetime, timezone
from uuid import uuid4


class TransactionStatus(str, Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    FAILED = "failed"
    REFUNDED = "refunded"


class Currency(str, Enum):
    USD = "USD"
    GBP = "GBP"
    EUR = "EUR"
    JPY = "JPY"
    CAD = "CAD"


class Transaction:
    def __init__(
        self,
        amount: float,
        currency: Currency,
        merchant_name: str,
        description: str = "",
        status: TransactionStatus = TransactionStatus.PENDING,
    ):
        self.id: str = str(uuid4())
        self.amount = amount
        self.currency = currency
        self.merchant_name = merchant_name
        self.description = description
        self.status = status
        self.created_at: datetime = datetime.now(timezone.utc)
        self.updated_at: datetime = datetime.now(timezone.utc)

    def update_status(self, new_status: TransactionStatus) -> None:
        self.status = new_status
        self.updated_at = datetime.now(timezone.utc)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "amount": self.amount,
            "currency": self.currency,
            "merchant_name": self.merchant_name,
            "description": self.description,
            "status": self.status,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }