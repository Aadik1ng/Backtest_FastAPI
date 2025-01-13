import os
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

class Backtester:
    def __init__(self, symbol, data, rolling_window=3, price_deviation=0.03):
        self.symbol = symbol
        self.data = data
        self.rolling_window = rolling_window
        self.price_deviation = price_deviation
        self.results = []

    def calculate_bollinger_bands(self):
        """Calculate the Bollinger Bands (SMA, UpperBand, LowerBand)"""
        self.data['MA'] = self.data['close'].rolling(window=self.rolling_window).mean()
        self.data['StdDev'] = self.data['close'].rolling(window=self.rolling_window).std()
        self.data['UpperBand'] = self.data['MA'] + (self.data['StdDev'] * 1)
        self.data['LowerBand'] = self.data['MA'] - (self.data['StdDev'] * 1)

    def run_backtest(self):
        """Run the backtest logic with trades worth 100 USD each"""
        self.results = []
        holdings = 0  # Tracks the value of tokens held in USD
        token_holdings = 0  # Tracks the quantity of tokens held

        for i in range(1, len(self.data)):
            current = self.data.iloc[i]

            # Buy signal: Close price falls below the lower band
            if current['close'] < current['LowerBand'] and token_holdings == 0:
                tokens_to_buy = 100 / current['close']  # Buy tokens worth 100 USD
                token_holdings += tokens_to_buy
                holdings = 100  # Record the USD equivalent of the purchase
                self.results.append({
                    'timestamp': current.name,
                    'action': 'Buy',
                    'price': current['close'],
                    'tokens_bought': tokens_to_buy,
                    'holdings_usd': holdings
                })
                print(f"Buy: {current.name} at {current['close']}, Tokens Bought: {tokens_to_buy:.6f}")

            # Sell signal: Close price rises above the upper band
            elif current['close'] > current['UpperBand'] and token_holdings > 0:
                sell_value = token_holdings * current['close']  # Calculate the value of tokens sold
                self.results.append({
                    'timestamp': current.name,
                    'action': 'Sell',
                    'price': current['close'],
                    'tokens_sold': token_holdings,
                    'sell_value': sell_value
                })
                print(f"Sell: {current.name} at {current['close']}, Tokens Sold: {token_holdings:.6f}, Sell Value: {sell_value:.2f}")
                holdings = 0  # Reset holdings after the sale
                token_holdings = 0

        # Liquidate remaining holdings at the end of the period
        if token_holdings > 0:
            final_price = self.data.iloc[-1]['close']
            sell_value = token_holdings * final_price
            self.results.append({
                'timestamp': self.data.index[-1],
                'action': 'Sell (End of Period)',
                'price': final_price,
                'tokens_sold': token_holdings,
                'sell_value': sell_value
            })
            print(f"Final Sell: {self.data.index[-1]} at {final_price}, Tokens Sold: {token_holdings:.6f}, Sell Value: {sell_value:.2f}")
            token_holdings = 0

        # Convert results to a DataFrame
        self.results_df = pd.DataFrame(self.results)

    
    
    def get_results(self):
        """Return backtest results as a DataFrame"""
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

        # Show the plot after saving
        plt.show()


