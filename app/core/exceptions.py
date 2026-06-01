from fastapi import HTTPException, status


class TransactionNotFoundError(HTTPException):
    def __init__(self, transaction_id: str):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Transaction with id '{transaction_id}' not found.",
        )


class InvalidStatusTransitionError(HTTPException):
    def __init__(self, current: str, requested: str):
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=(
                f"Cannot transition from '{current}' to '{requested}'. "
                "Completed and failed transactions cannot be modified."
            ),
        )


class DuplicateTransactionError(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail="A transaction with identical details already exists.",
        )