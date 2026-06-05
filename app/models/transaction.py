"""
transaction.py (models)

Defines the core Transaction domain model for the BankGuard API.
This is the blueprint of a transaction object used throughout the system.
All transaction data is structured, validated, and managed through this model.
"""

from enum import Enum
from datetime import datetime, timezone
from uuid import uuid4

# Defines the valid lifecycle states of a transaction.
# A transaction moves from PENDING towards COMPLETED, FAILED, or REFUNDED.
class TransactionStatus(str, Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    FAILED = "failed"
    REFUNDED = "refunded"

# Defines the accepted currencies for transactions.
# Only these specific currencies are valid. Any other value is rejected.
class Currency(str, Enum):
    USD = "USD"
    GBP = "GBP"
    EUR = "EUR"
    JPY = "JPY"
    CAD = "CAD"

# The core transaction blueprint.
# Every transaction created in BankGuard is built from this class.
# It automatically generates a unique ID and records timestamps on creation.
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


    # Updates the transaction status and records the exact time of the change.
    def update_status(self, new_status: TransactionStatus) -> None:
        self.status = new_status
        self.updated_at = datetime.now(timezone.utc)



    # Converts the transaction object into a plain dictionary.
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