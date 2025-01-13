import os
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from fastapi import APIRouter, HTTPException
from app.routers.data_ingestion import DataIngestion

class Backtester:
    def __init__(self, symbol, data, rolling_window=20, price_deviation=0.03):
        self.symbol = symbol
        self.data = data.copy()
        self.rolling_window = rolling_window
        self.price_deviation = price_deviation
        self.results = []

    def calculate_bollinger_bands(self):
        self.data['MA'] = self.data['close'].rolling(window=self.rolling_window).mean()
        self.data['StdDev'] = self.data['close'].rolling(window=self.rolling_window).std()
        self.data['UpperBand'] = self.data['MA'] + (self.data['StdDev'] * 1)
        self.data['LowerBand'] = self.data['MA'] - (self.data['StdDev'] * 1)

    def run_backtest(self):
        holdings = 0
        token_holdings = 0

        for i in range(1, len(self.data)):
            current = self.data.iloc[i]
            if current['close'] < (current['LowerBand'] * (1 - self.price_deviation)) and token_holdings == 0:
                tokens_to_buy = 100 / current['close']
                token_holdings += tokens_to_buy
                self.results.append({
                    'token': self.symbol,
                    'date_in': current.name,
                    'buy_price': current['close'],
                    'date_out': None,
                    'sell_price': None,
                    'profit_percentage': None
                })

            elif current['close'] > current['UpperBand'] and token_holdings > 0:
                last_buy = self.results[-1]
                profit = (current['close'] - last_buy['buy_price']) / last_buy['buy_price'] * 100
                last_buy.update({
                    'date_out': current.name,
                    'sell_price': current['close'],
                    'profit_percentage': profit
                })
                token_holdings = 0

        # Liquidate at the end of the backtest period
        if token_holdings > 0:
            final_price = self.data.iloc[-1]['close']
            last_buy = self.results[-1]
            profit = (final_price - last_buy['buy_price']) / last_buy['buy_price'] * 100
            last_buy.update({
                'date_out': self.data.index[-1],
                'sell_price': final_price,
                'profit_percentage': profit
            })

    def get_results(self):
        return pd.DataFrame(self.results)

    def plot_bollinger_bands(self):
        """Plot the close prices along with Bollinger Bands for visual inspection"""
        plt.figure(figsize=(10, 6))
        plt.plot(self.data['close'], label='Close Price')
        plt.plot(self.data['MA'], label='Moving Average', color='orange')
        plt.plot(self.data['UpperBand'], label='Upper Band', linestyle='--', color='red')
        plt.plot(self.data['LowerBand'], label='Lower Band', linestyle='--', color='green')

        # Set title and legend
        plt.title(f'{self.symbol} Bollinger Bands and Close Price')
        plt.legend()

        # Format the x-axis to display only Month and Day (no Year)
        ax = plt.gca()
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%m-%d'))  # Formatting date to MM-DD
        ax.xaxis.set_major_locator(mdates.WeekdayLocator())  # Adjust label frequency

        # Rotate x-axis labels for better readability
        plt.xticks(rotation=45)

        # Optionally adjust label formatting if overlapping
        plt.tight_layout()

        # Show plot
        plt.show()

    def save_results(self):
        """Save the backtest results and the corresponding graph"""
        # Ensure 'results' folder exists
        os.makedirs('results', exist_ok=True)

        # Save backtest results as a CSV file in the 'results' folder
        results_df = self.get_results()
        results_csv_path = os.path.join('results', f'{self.symbol}_backtest_results.csv')
        results_df.to_csv(results_csv_path, index=False)
        print(f"Backtest results saved to {results_csv_path}")

        # Create the plot and save it
        plt.figure(figsize=(10, 6))  # Create the figure first

        # Plot the close prices along with Bollinger Bands for visual inspection
        plt.plot(self.data['close'], label='Close Price')
        plt.plot(self.data['MA'], label='Moving Average', color='orange')
        plt.plot(self.data['UpperBand'], label='Upper Band', linestyle='--', color='red')
        plt.plot(self.data['LowerBand'], label='Lower Band', linestyle='--', color='green')

        # Set title and legend
        plt.title(f'{self.symbol} Bollinger Bands and Close Price')
        plt.legend()

        # Format the x-axis to display only Month and Day (no Year)
        ax = plt.gca()
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%m-%d'))  # Formatting date to MM-DD
        ax.xaxis.set_major_locator(mdates.WeekdayLocator())  # Adjust label frequency, you can change to MonthLocator()

        # Rotate x-axis labels for better readability
        plt.xticks(rotation=45)

        # Optionally adjust label formatting if overlapping
        plt.tight_layout()

        # Save the graph as a PNG file with the same name
        graph_path = os.path.join('results', f'{self.symbol}_bollinger_bands.png')
        plt.savefig(graph_path)  # Save the figure to PNG before calling plt.show()
        print(f"Graph saved to {graph_path}")
        graph_url = f"/static/{self.symbol}_bollinger_bands.png"
        return graph_url

        


router = APIRouter()

@router.post("/run/")
def run_backtest(symbol: str, rolling_window: int = 20, price_deviation: float = 0.03):
    """
    Run the backtest for the given symbol and parameters.
    """
    data = DataIngestion().load_data(symbol)
    if data is None:
        raise HTTPException(status_code=404, detail=f"No data found for {symbol}. Please fetch data first.")
    
    backtester = Backtester(symbol, data, rolling_window, price_deviation)
    backtester.calculate_bollinger_bands()
    backtester.run_backtest()
    backtester.save_results()
    return {"message": f"Backtest completed for {symbol}.", "results": backtester.get_results().to_dict(orient="records")}