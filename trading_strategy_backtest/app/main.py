from fastapi import FastAPI
from app.routers import data_ingestion, backtesting

app = FastAPI()

# Include routers
app.include_router(data_ingestion.router, prefix="/data", tags=["Data Ingestion"])
app.include_router(backtesting.router, prefix="/backtest", tags=["Backtesting"])

@app.get("/")
def root():
    """
    Root endpoint to verify the API is running.
    """
    return {"message": "Welcome to the Trading Strategy Backtesting API"}
