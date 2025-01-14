from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os
from app.routers import data_ingestion, backtesting

# Ensure the 'results' directory exists
if not os.path.exists('results'):
    os.makedirs('results')

app = FastAPI()

# Include routers
app.include_router(data_ingestion.router, prefix="/data", tags=["Data Ingestion"])
app.include_router(backtesting.router, prefix="/backtest", tags=["Backtesting"])

# Mount 'results' as a static directory
app.mount("/static", StaticFiles(directory=os.path.abspath("results")), name="static")

# Update CORS middleware to allow the Vercel frontend


app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
)

@app.get("/")
def root():
    """
    Root endpoint to verify the API is running.
    """
    return {"message": "Welcome to the Trading Strategy Backtesting API"}

@app.get("/static/{filename}")
def serve_file(filename: str):
    """
    Explicitly serve files from the 'results' directory.
    """
    file_path = os.path.join("results", filename)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")
    return FileResponse(file_path)
