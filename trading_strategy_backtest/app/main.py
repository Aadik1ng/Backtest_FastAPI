from fastapi import FastAPI
from app.routers import data_ingestion, backtesting
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

app = FastAPI()

# Include routers
app.include_router(data_ingestion.router, prefix="/data", tags=["Data Ingestion"])
app.include_router(backtesting.router, prefix="/backtest", tags=["Backtesting"])
app.mount("/static", StaticFiles(directory="results"), name="static")

# Update CORS middleware to allow your Vercel frontend


origins = [
    "https://react-frontend-liard-two.vercel.app"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Allow specific origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods (you can restrict this to specific methods like ["GET", "POST"])
    allow_headers=["*"],  # Allow all headers
)

@app.get("/")
def root():
    """
    Root endpoint to verify the API is running.
    """
    return {"message": "Welcome to the Trading Strategy Backtesting API"}
