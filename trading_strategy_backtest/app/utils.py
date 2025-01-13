# app/utils.py

from pydantic import BaseModel
from typing import List

class FetchDataRequest(BaseModel):
    symbols: List[str]  # List of symbols (e.g., ["BTCUSDT", "ETHUSDT"])
    start_date: str  # Start date in 'YYYY-MM-DD' format
    end_date: str    # End date in 'YYYY-MM-DD' format
    interval: str = "1d"  # Default interval is '1d'
