"""
main.py

The entry point of the BankGuard API.

This file creates the FastAPI application, registers all the routers,
adds middleware, and defines the health check endpoints.

run the command:
    uvicorn app.main:app --reload

Python starts here. Everything begins from this file.
"""


from fastapi import FastAPI 
from contextlib import asynccontextmanager
from app.routers import predictions

# importing CORSMiddleware to allow the API to accept requests from 
# other origins like frontend websites or external bank systems.
from fastapi.middleware.cors import CORSMiddleware
from app.routers import transactions
from app.core.config import settings


# here lifespan manages the startup and shutdown of the entire BankGuard API.
# It is a custom context manager: everything before yield runs at startup,
# everything after yield runs at shutdown, guaranteed.
@asynccontextmanager
async def lifespan(app: FastAPI):
    print(f"Starting {settings.PROJECT_NAME} v{settings.VERSION}")
    yield
    print("Shutting down BankGuard API...")



# This block officially creates the BankGuard API application.
# It gives the app its identity: name, description, version, 
# and documentation URLs that appear on the Swagger page at /docs.
app = FastAPI(
    title=settings.PROJECT_NAME,
    description=settings.DESCRIPTION,
    version=settings.VERSION,
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,  ## connects the startup and shutdown manager to the app
)


# Adding a middleware for the security
# CORSMiddleware allowing requests from any origin (any website or system).
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


#  plug endpoint files transactions and predictions into the main app
app.include_router(transactions.router, prefix="/api/v1")
app.include_router(predictions.router, prefix="/api/v1")


# Home page of the API. Returns basic information about BankGuard.
@app.get("/", tags=["Health"])
async def root():
    return {
        "service": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "status": "operational",
        "docs": "/docs",
    }

# Lightweight pulse check endpoint.
# Monitoring systems call this automatically every 60 seconds
# to confirm the API is alive.
@app.get("/health", tags=["Health"])
async def health_check():
    return {"status": "ok"}