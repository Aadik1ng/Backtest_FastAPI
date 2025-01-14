# Trading Strategy Backtesting API

## Overview

This project provides a FastAPI-based backend for backtesting trading strategies using historical market data. The application includes modules for data ingestion, backtesting, and result visualization, with a focus on Bollinger Bands-based strategies.

### Runnig:- https://backtestfastapi-production.up.railway.app/docs#

## Features

1. **Data Ingestion**:
   - Fetch historical market data from Binance.
   - Save and load data locally for future use.

2. **Backtesting**:
   - Execute a Bollinger Bands-based trading strategy.
   - Analyze trades, calculate profits, and generate results.

3. **Visualization**:
   - Plot Bollinger Bands with close price data.
   - Save results and graphs for easy access.

4. **Static File Hosting**:
   - Host backtest results and plots via the `/static` endpoint.

5. **Frontend Integration**:
   - Cross-Origin Resource Sharing (CORS) enabled for integration with frontend applications.

---

## API Endpoints

### **Root Endpoint**
- `GET /`
  - Description: Verify that the API is running.
  - Response: `{ "message": "Welcome to the Trading Strategy Backtesting API" }`

---

### **Data Ingestion**

#### **Fetch and Save Data**
- `POST /data/fetch/`
  - Request Body:
    ```json
    {
      "symbols": ["BTCUSDT", "ETHUSDT"],
      "start_date": "2023-01-01",
      "end_date": "2023-12-31",
      "interval": "1d"
    }
    ```
  - Description: Fetch historical data for specified symbols and save it locally.
  - Response: `{ "message": "Data for BTCUSDT, ETHUSDT saved successfully." }`

#### **Load Data**
- `GET /data/load/`
  - Query Parameters:
    - `symbol` (e.g., BTCUSDT)
  - Description: Load saved data for a given symbol.
  - Response: JSON representation of the loaded data.

---

### **Backtesting**

#### **Run Backtest**
- `POST /backtest/run/`
  - Query Parameters:
    - `symbol` (e.g., BTCUSDT)
    - `rolling_window` (default: 20)
    - `price_deviation` (default: 0.03)
  - Description: Run a backtest for the specified symbol using Bollinger Bands.
  - Response:
    ```json
    {
      "message": "Backtest completed for BTCUSDT.",
      "graph_url": "https://your-deployment-url/static/BTCUSDT_bollinger_bands.png"
    }
    ```

---

### **Static Files**
- `GET /static/{filename}`
  - Description: Serve backtest results and graphs stored in the `results` directory.

---

## Getting Started

### Prerequisites
- Python 3.9 or higher
- Virtual environment manager (e.g., `venv`)

### Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo/trading_strategy_backtest.git
   cd trading_strategy_backtest
  
2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
3.Install dependencies:
```bash
  pip install -r requirements.txt
```
4. Running the Application
   ```bash
   uvicorn app.main:app --reload
   
### **Notes**

Due to Binance API throwing a 451 Client Error when accessed from certain regions, the required CSV files have been manually uploaded to the data directory for this project.
If you run the application locally in a region where Binance API access is unrestricted, the API will function as expected and fetch the data dynamically.
Copy code






