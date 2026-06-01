# BankGuard API

A production-ready fraud detection REST API for banking transactions, 
built with FastAPI, XGBoost, and SHAP explainability. Designed with 
clean architecture, test-driven development, and full containerisation 
via Docker.

---

## Features

- Full CRUD operations for banking transactions
- Fraud risk scoring powered by XGBoost
- SHAP explainability on every prediction
- Input validation with Pydantic
- Pagination and filtering on transaction queries
- Custom exception handling with proper HTTP status codes
- Test suite with pytest (TDD approach)
- Containerised with Docker
- Auto-generated interactive API docs via Swagger UI

---

## Tech Stack

| Layer | Technology |
|---|---|
| API Framework | FastAPI |
| ML Model | XGBoost |
| Explainability | SHAP TreeExplainer |
| Validation | Pydantic v2 |
| Database | PostgreSQL + SQLAlchemy |
| Testing | pytest |
| Containerisation | Docker |
| Deployment | GCP Cloud Run |
| Language | Python 3.11 |





## Project Structure

```
bankguard-api/
├── app/
│   ├── core/
│   │   ├── config.py
│   │   └── exceptions.py
│   ├── models/
│   │   └── transaction.py
│   ├── routers/
│   │   └── transactions.py
│   ├── schemas/
│   │   └── transaction.py
│   ├── services/
│   │   └── transaction_service.py
│   └── main.py
├── ml/
├── tests/
│   └── test_transactions.py
├── Dockerfile
├── requirements.txt
└── README.md
```

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/isha-atif-dev/bankguard-api.git
cd bankguard-api
```

### 2. Create and activate virtual environment

```bash
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Mac/Linux
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the API

```bash
uvicorn app.main:app --reload
```

### 5. Open interactive docs
http://127.0.0.1:8000/docs

---

## Running with Docker

```bash
docker build -t bankguard-api .
docker run -p 8000:8000 bankguard-api
```

---

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | /health | Health check |
| POST | /api/v1/transactions/ | Create a transaction |
| GET | /api/v1/transactions/ | Get all transactions |
| GET | /api/v1/transactions/{id} | Get transaction by ID |
| PATCH | /api/v1/transactions/{id}/status | Update transaction status |
| DELETE | /api/v1/transactions/{id} | Delete a transaction |

---

## Running Tests

```bash
pytest tests/ -v
```

All 7 tests pass with 0 errors.

---

## Author

Isha Atif
MRes Applied AI, University of Greater Manchester
[LinkedIn](https://linkedin.com/in/isha-atif) | 
[GitHub](https://github.com/isha-atif-dev)