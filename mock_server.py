
import asyncio
import websockets
import json
import random
import datetime

# Mock stock data
stocks = {
    "AAPL": {"price": 150.0, "last_update": datetime.datetime.now()},
    "GOOGL": {"price": 2800.0, "last_update": datetime.datetime.now()},
    "MSFT": {"price": 300.0, "last_update": datetime.datetime.now()},
    "AMZN": {"price": 3400.0, "last_update": datetime.datetime.now()}
}

async def generate_stock_updates(websocket):
    print(f"Client connected: {websocket.remote_address}")
    try:
        while True:
            # Select a random stock to update
            ticker = random.choice(list(stocks.keys()))
            stock = stocks[ticker]

            # Simulate price change (small random fluctuation)
            change_percent = random.uniform(-0.015, 0.015) # +/- 1.5%
            new_price = round(stock["price"] * (1 + change_percent), 2)

            # Ensure price doesn't go below zero
            new_price = max(0.01, new_price)

            stock["price"] = new_price
            stock["last_update"] = datetime.datetime.now()

            update_message = {
                "ticker": ticker,
                "price": new_price,
                "timestamp": stock["last_update"].isoformat()
            }

            await websocket.send(json.dumps(update_message))
            # print(f"Sent update: {update_message}")

            # Wait for a short interval before sending the next update
            await asyncio.sleep(random.uniform(0.5, 2.0)) # Send updates every 0.5-2 seconds
    except websockets.exceptions.ConnectionClosedOK:
        print(f"Client disconnected: {websocket.remote_address}")
    except websockets.exceptions.ConnectionClosedError as e:
        print(f"Client connection error: {websocket.remote_address}, Error: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        print(f"Stopped sending updates to {websocket.remote_address}")

async def main():
    host = "0.0.0.0"
    port = 8765
    async with websockets.serve(generate_stock_updates, host, port):
        print(f"Mock WebSocket server started on ws://{host}:{port}")
        await asyncio.Future()  # Run forever

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Server stopped manually.")

