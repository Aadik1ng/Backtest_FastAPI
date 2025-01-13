# app/routers/data_ingestion.py

import os
import pandas as pd
import requests
from datetime import datetime
from fastapi import APIRouter, HTTPException
from app.utils import FetchDataRequest  # Importing FetchDataRequest from utils.py

class DataIngestion:
    DATA_DIR = "data"
    BASE_URL = "https://api.binance.com/api/v3/klines"

    def __init__(self):
        os.makedirs(self.DATA_DIR, exist_ok=True)

    def fetch_data(self, symbol, start_date, end_date, interval="1d"):
        # Convert dates to timestamp in milliseconds
        params = {
            "symbol": symbol,
            "interval": interval,
            "startTime": int(start_date.timestamp() * 1000),
            "endTime": int(end_date.timestamp() * 1000),
        }
        response = requests.get(self.BASE_URL, params=params)
        response.raise_for_status()  # Raise an exception for bad responses
        return response.json()

    def save_data(self, symbol, data):
        df = pd.DataFrame(data, columns=[
            "timestamp", "open", "high", "low", "close", "volume",
            "close_time", "quote_asset_volume", "trades", "taker_base_vol", "taker_quote_vol", "ignore"
        ])
        df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
        df.set_index("timestamp", inplace=True)
        df.to_csv(os.path.join(self.DATA_DIR, f"{symbol}.csv"))

    def load_data(self, symbol):
        file_path = os.path.join(self.DATA_DIR, f"{symbol}.csv")
        if os.path.exists(file_path):
            return pd.read_csv(file_path, index_col="timestamp", parse_dates=True)
        return None

router = APIRouter()
data_ingestion = DataIngestion()

@router.post("/fetch/")
def fetch_and_save(request: FetchDataRequest):
    """
    Fetch historical data for multiple symbols and save it locally.
    """
    try:
        start_dt = datetime.strptime(request.start_date, "%Y-%m-%d")
        end_dt = datetime.strptime(request.end_date, "%Y-%m-%d")
        for symbol in request.symbols:
            data = data_ingestion.fetch_data(symbol, start_dt, end_dt, request.interval)
            data_ingestion.save_data(symbol, data)
        return {"message": f"Data for {', '.join(request.symbols)} saved successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/load/")
def load_data(symbol: str):
    """
    Load locally saved data for a given symbol.
    """
    try:
        data = data_ingestion.load_data(symbol)
        if data is not None:
            return {"message": f"Data for {symbol} loaded successfully.", "data": data.to_dict(orient="records")}
        else:
            return {"message": f"No data found for {symbol}."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
