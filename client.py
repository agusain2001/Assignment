
import asyncio
import websockets
import json
from datetime import datetime, timedelta
from collections import defaultdict, deque

# Store recent prices for each ticker (ticker -> deque of (timestamp, price))
price_history = defaultdict(lambda: deque(maxlen=100)) # Keep last 100 updates per ticker
notification_threshold_percent = 2.0
notification_time_window = timedelta(minutes=1)

async def process_stock_updates():
    uri = "ws://localhost:8765"
    while True:
        try:
            async with websockets.connect(uri) as websocket:
                print(f"Connected to WebSocket server at {uri}")
                while True:
                    try:
                        message = await websocket.recv()
                        data = json.loads(message)
                        # print(f"Received: {data}")

                        ticker = data["ticker"]
                        price = data["price"]
                        timestamp_str = data["timestamp"]
                        timestamp = datetime.fromisoformat(timestamp_str)

                        # Store the new price update
                        history = price_history[ticker]
                        history.append((timestamp, price))

                        # Check for significant price increase within the time window
                        check_price_increase(ticker, timestamp, price, history)

                    except websockets.exceptions.ConnectionClosed:
                        print("Connection closed by server. Reconnecting...")
                        break # Break inner loop to reconnect
                    except json.JSONDecodeError:
                        print(f"Received non-JSON message: {message}")
                    except Exception as e:
                        print(f"Error processing message: {e}")
                        # Optional: Add a small delay before trying to receive next message
                        await asyncio.sleep(1)

        except (websockets.exceptions.ConnectionClosedError, ConnectionRefusedError, OSError) as e:
            print(f"Failed to connect or connection lost: {e}. Retrying in 5 seconds...")
            await asyncio.sleep(5)
        except Exception as e:
            print(f"An unexpected error occurred: {e}. Retrying in 10 seconds...")
            await asyncio.sleep(10)

def check_price_increase(ticker, current_timestamp, current_price, history):
    """Checks if the price increased by more than the threshold within the window."""
    # Find the earliest price within the notification time window
    window_start_time = current_timestamp - notification_time_window
    earliest_price_in_window = None

    # Iterate through history (which is ordered by time) to find relevant prices
    for ts, price in history:
        if ts >= window_start_time:
            if earliest_price_in_window is None:
                 earliest_price_in_window = price # First price within the window
            # Check increase against the earliest price found in the window
            if current_price > earliest_price_in_window * (1 + notification_threshold_percent / 100):
                percentage_increase = ((current_price - earliest_price_in_window) / earliest_price_in_window) * 100
                print(f"*** ALERT ***: {ticker} price increased by {percentage_increase:.2f}% ",
                      f"(from {earliest_price_in_window} to {current_price}) ",
                      f"within the last {notification_time_window.total_seconds()} seconds.")
                # Avoid repeated alerts for the same rise by potentially adding a cooldown
                # For simplicity, we just print the alert every time the condition is met
                break # Alert triggered for this update, no need to check further back

async def main():
    await process_stock_updates()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Client stopped manually.")

