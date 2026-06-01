from typing import Optional
from app.models.transaction import Transaction, TransactionStatus, Currency
from app.schemas.transaction import TransactionCreate
from app.core.exceptions import (
    TransactionNotFoundError,
    InvalidStatusTransitionError,
)

TERMINAL_STATES = {TransactionStatus.COMPLETED, TransactionStatus.FAILED}

db: dict[str, Transaction] = {}


class TransactionService:

    def create_transaction(self, data: TransactionCreate) -> Transaction:
        transaction = Transaction(
            amount=data.amount,
            currency=data.currency,
            merchant_name=data.merchant_name,
            description=data.description,
        )
        db[transaction.id] = transaction
        return transaction

    def get_transaction(self, transaction_id: str) -> Transaction:
        transaction = db.get(transaction_id)
        if not transaction:
            raise TransactionNotFoundError(transaction_id)
        return transaction

    def get_all_transactions(
        self,
        page: int = 1,
        page_size: int = 10,
        status: Optional[TransactionStatus] = None,
        currency: Optional[Currency] = None,
    ) -> dict:
        results = list(db.values())

        if status:
            results = [t for t in results if t.status == status]
        if currency:
            results = [t for t in results if t.currency == currency]

        total = len(results)
        start = (page - 1) * page_size
        end = start + page_size
        paginated = results[start:end]

        return {
            "total": total,
            "page": page,
            "page_size": page_size,
            "results": [t.to_dict() for t in paginated],
        }

    def update_status(
        self, transaction_id: str, new_status: TransactionStatus
    ) -> Transaction:
        transaction = self.get_transaction(transaction_id)
        if transaction.status in TERMINAL_STATES:
            raise InvalidStatusTransitionError(
                transaction.status, new_status
            )
        transaction.update_status(new_status)
        return transaction

    def delete_transaction(self, transaction_id: str) -> dict:
        transaction = self.get_transaction(transaction_id)
        del db[transaction.id]
        return {"message": f"Transaction {transaction_id} deleted successfully."}


transaction_service = TransactionService()