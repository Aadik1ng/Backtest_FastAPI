import os
import pandas as pd
import requests
from datetime import datetime

class DataIngestion:
    DATA_DIR = "data"
    BASE_URL = "https://api.binance.com/api/v3/klines"

    @staticmethod
    def fetch_data(symbol, start_date, end_date, interval="1d"):
        params = {
            "symbol": symbol,
            "interval": interval,
            "startTime": int(start_date.timestamp() * 1000),
            "endTime": int(end_date.timestamp() * 1000)
        }
        response = requests.get(DataIngestion.BASE_URL, params=params)
        response.raise_for_status()
        return response.json()

    @staticmethod
    def save_data(symbol, data):
        os.makedirs(DataIngestion.DATA_DIR, exist_ok=True)
        df = pd.DataFrame(data, columns=[
            "timestamp", "open", "high", "low", "close", "volume",
            "close_time", "quote_asset_volume", "trades", "taker_base_vol", "taker_quote_vol", "ignore"
        ])
        df["timestamp"] = pd.to_datetime(df["timestamp"], unit='ms')
        df.set_index("timestamp", inplace=True)
        df.to_csv(os.path.join(DataIngestion.DATA_DIR, f"{symbol}.csv"))

    @staticmethod
    def load_data(symbol):
        file_path = os.path.join(DataIngestion.DATA_DIR, f"{symbol}.csv")
        if os.path.exists(file_path):
            return pd.read_csv(file_path, index_col="timestamp", parse_dates=True)
        return None