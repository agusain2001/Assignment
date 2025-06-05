
import pandas as pd
import numpy as np

def moving_average_crossover_strategy(data_file, short_window=50, long_window=200, initial_capital=10000):
    """
    Implements a Moving Average Crossover strategy.

    Args:
        data_file (str): Path to the CSV file with historical stock data.
                         Expected columns: Date, Close.
        short_window (int): The window size for the short moving average.
        long_window (int): The window size for the long moving average.
        initial_capital (float): The starting capital for the simulation.

    Returns:
        tuple: (pandas.DataFrame containing signals, float total profit/loss)
    """
    try:
        # Load data
        df = pd.read_csv(data_file, parse_dates=["Date"], index_col="Date")
        if 'Close' not in df.columns:
            raise ValueError("CSV must contain a 'Close' column.")

        # Calculate Moving Averages
        df['SMA_Short'] = df['Close'].rolling(window=short_window, min_periods=1).mean()
        df['SMA_Long'] = df['Close'].rolling(window=long_window, min_periods=1).mean()

        # Generate Signals
        # Signal = 1 when SMA_Short > SMA_Long, 0 otherwise
        df['Signal'] = 0
        # Use np.where for vectorized comparison, handle potential NaNs from rolling mean
        df['Signal'] = np.where(df['SMA_Short'] > df['SMA_Long'], 1, 0)

        # Generate Trading Orders (Buy=1, Sell=-1)
        # Difference tells us when the signal changes
        df['Position'] = df['Signal'].diff()

        # Simulation
        capital = initial_capital
        position_active = 0 # 0 = no position, 1 = long position
        shares = 0
        trade_log = []

        for i in range(len(df)):
            date = df.index[i]
            close_price = df['Close'].iloc[i]
            trade_signal = df['Position'].iloc[i]

            # Check for NaN signal (can happen at the start)
            if pd.isna(trade_signal):
                continue

            # Buy Signal
            if trade_signal == 1 and position_active == 0:
                shares_to_buy = capital // close_price
                if shares_to_buy > 0:
                    cost = shares_to_buy * close_price
                    capital -= cost
                    shares = shares_to_buy
                    position_active = 1
                    trade_log.append(f"{date.strftime('%Y-%m-%d')}: BUY {shares} shares @ {close_price:.2f}, Cost: {cost:.2f}, Capital: {capital:.2f}")
                    # print(trade_log[-1]) # Optional: print trades as they happen

            # Sell Signal
            elif trade_signal == -1 and position_active == 1:
                revenue = shares * close_price
                capital += revenue
                trade_log.append(f"{date.strftime('%Y-%m-%d')}: SELL {shares} shares @ {close_price:.2f}, Revenue: {revenue:.2f}, Capital: {capital:.2f}")
                # print(trade_log[-1]) # Optional: print trades as they happen
                shares = 0
                position_active = 0

        # Calculate final portfolio value if still holding shares
        final_portfolio_value = capital + (shares * df['Close'].iloc[-1])
        total_profit_loss = final_portfolio_value - initial_capital
        profit_loss_percent = (total_profit_loss / initial_capital) * 100

        print(f"Simulation Complete.")
        print(f"Initial Capital: ${initial_capital:.2f}")
        print(f"Final Portfolio Value: ${final_portfolio_value:.2f}")
        print(f"Total Profit/Loss: ${total_profit_loss:.2f} ({profit_loss_percent:.2f}%)")

        # Prepare report
        report_content = "Moving Average Crossover Strategy Simulation Report\n"
        report_content += "==================================================\n"
        report_content += f"Data File: {data_file}\n"
        report_content += f"Short Window: {short_window}, Long Window: {long_window}\n"
        report_content += f"Initial Capital: ${initial_capital:.2f}\n\n"
        report_content += "Trade Log:\n"
        report_content += "----------\n"
        if trade_log:
            report_content += "\n".join(trade_log)
        else:
            report_content += "No trades executed.\n"
        report_content += "\n\nPerformance Summary:\n"
        report_content += "--------------------\n"
        report_content += f"Final Portfolio Value: ${final_portfolio_value:.2f}\n"
        report_content += f"Total Profit/Loss: ${total_profit_loss:.2f}\n"
        report_content += f"Total Return: {profit_loss_percent:.2f}%\n"

        return df, report_content, total_profit_loss

    except FileNotFoundError:
        print(f"Error: Data file not found at {data_file}")
        return None, "Error: Data file not found.", 0
    except Exception as e:
        print(f"An error occurred during simulation: {e}")
        return None, f"Error during simulation: {e}", 0

# --- Main execution block ---
if __name__ == "__main__":
    data_csv_path = 'historical_data.csv'
    report_file_path = 'simulation_report.txt'
    output_csv_path = 'data_with_signals.csv' # Save df with signals

    # Define strategy parameters (use shorter windows for the limited data provided)
    # Using 10 and 30 day MAs as an example with ~130 data points
    short_ma = 10
    long_ma = 30

    print(f"Running simulation with Short MA={short_ma}, Long MA={long_ma}...")
    results_df, report_text, pnl = moving_average_crossover_strategy(data_csv_path, short_window=short_ma, long_window=long_ma)

    if results_df is not None:
        # Save the dataframe with signals
        try:
            results_df.to_csv(output_csv_path)
            print(f"Data with signals saved to {output_csv_path}")
        except Exception as e:
            print(f"Error saving results CSV: {e}")

        # Save the report text file
        try:
            with open(report_file_path, 'w') as f:
                f.write(report_text)
            print(f"Simulation report saved to {report_file_path}")
        except Exception as e:
            print(f"Error saving report file: {e}")
    else:
        print("Simulation failed. No results to save.")
        # Still save the error report if generated
        if report_text.startswith("Error"):
             try:
                with open(report_file_path, 'w') as f:
                    f.write(report_text)
                print(f"Error report saved to {report_file_path}")
             except Exception as e:
                print(f"Error saving error report file: {e}")

