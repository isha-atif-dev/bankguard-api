"""
exceptions.py

Defines all custom HTTP exceptions for the BankGuard API.
All errors are defined in one place so that error handling
is consistent, reusable, and easy to maintain across the entire system.
"""


from fastapi import HTTPException, status

# Raised when a requested transaction does not exist in the system.
# Returns 404 Not Found with the specific transaction ID in the message.
class TransactionNotFoundError(HTTPException):
    def __init__(self, transaction_id: str):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Transaction with id '{transaction_id}' not found.",
        )


# Raised when attempting to update a transaction that has already
# reached a terminal state. Completed and failed transactions
# cannot be modified. Returns 422 Unprocessable Entity.
class InvalidStatusTransitionError(HTTPException):
    def __init__(self, current: str, requested: str):
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=(
                f"Cannot transition from '{current}' to '{requested}'. "
                "Completed and failed transactions cannot be modified."
            ),
        )


# Raised when a transaction with identical details already exists
# in the system, preventing duplicate records.
# Returns 409 Conflict.
class DuplicateTransactionError(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail="A transaction with identical details already exists.",
        )