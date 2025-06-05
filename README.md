
# Assignment Submission

## Objective

This project implements a basic trading system as per the assignment requirements, covering REST API development, real-time data processing, cloud integration simulation, and an optional algorithmic trading simulation.

## Structure

The submission is divided into separate tasks, each contained within a corresponding zip file:

-   `task1`: REST API Development (FastAPI + PostgreSQL)
-   `task2`: Real-Time Data Processing (WebSocket Simulation)
-   `task3`: Cloud Integration (AWS Lambda Simulation)
-   `task4`: Algorithmic Trading Simulation (Moving Average Crossover)

## Task 1: REST API Development (`task1`)

This task implements a REST API using FastAPI to manage trade operations, storing data in a PostgreSQL database.

### Components

-   `app/`: Contains the FastAPI application code.
    -   `main.py`: FastAPI application setup and endpoints.
    -   `schemas.py`: Pydantic models for data validation.
    -   `models.py`: SQLAlchemy models for database tables.
    -   `crud.py`: Functions for database operations (Create, Read).
    -   `database.py`: Database connection setup (SQLAlchemy).
-   `requirements.txt`: Python dependencies.
-   `server.log`: Log file from the test run (can be ignored).

### Setup and Execution

1.  **Prerequisites:** Ensure Docker and Python 3.11+ are installed.
2.  **Unzip:** Extract the contents of `task1`.
3.  **Database:**
    *   Start a PostgreSQL container using Docker:
        ```bash
        sudo docker run --name tradedb-postgres -e POSTGRES_USER=user -e POSTGRES_PASSWORD=password -e POSTGRES_DB=tradedb -p 5432:5432 -d postgres:14
        ```
    *   This uses the default credentials (`user`/`password`) and database name (`tradedb`) configured in `app/database.py`. You can modify `DATABASE_URL` in `app/database.py` or set it as an environment variable if your setup differs.
4.  **Navigate:** Open a terminal in the extracted `task1_api` directory.
5.  **Virtual Environment (Recommended):**
    ```bash
    python3.11 -m venv venv
    source venv/bin/activate  # On Linux/macOS
    # venv\Scripts\activate  # On Windows
    ```
6.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
7.  **Run API Server:**
    ```bash
    uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
    ```
    The API will be accessible at `http://localhost:8000`. Documentation is available at `http://localhost:8000/docs`.

### Endpoints

-   `POST /trades/`: Add a new trade. Requires a JSON body like `{"ticker": "AAPL", "price": 150.50, "quantity": 100, "side": "buy"}`.
-   `GET /trades/`: Fetch trades. Optional query parameters:
    -   `ticker` (string): Filter by stock ticker.
    -   `start_date` (string, ISO format): Filter trades from this timestamp onwards.
    -   `end_date` (string, ISO format): Filter trades up to this timestamp.
    -   `skip` (int): Number of records to skip (for pagination).
    -   `limit` (int): Maximum number of records to return.

### Assumptions

-   PostgreSQL is accessible on `localhost:5432` with the specified credentials.
-   Input validation is primarily handled by Pydantic models.

## Task 2: Real-Time Data Processing (`task2`)

This task simulates real-time stock data processing using WebSockets.

### Components

-   `mock_server.py`: A WebSocket server that sends simulated stock price updates.
-   `client.py`: A WebSocket client that connects to the server, receives updates, and monitors for significant price increases (>2% within 1 minute).

### Setup and Execution

1.  **Prerequisites:** Ensure Python 3.11+ is installed.
2.  **Unzip:** Extract the contents of `task2`.
3.  **Navigate:** Open a terminal in the extracted `task2_websocket` directory.
4.  **Install Dependencies:**
    ```bash
    pip install websockets
    ```
5.  **Run Server:** In the first terminal, start the mock server:
    ```bash
    python3.11 mock_server.py
    ```
    The server will start on `ws://localhost:8765`.
6.  **Run Client:** Open a *second* terminal in the same directory and start the client:
    ```bash
    python3.11 client.py
    ```
    The client will connect to the server and start printing received messages and alerts for price increases.

### Assumptions

-   The server runs on `localhost:8765`.
-   The client attempts to connect to `ws://localhost:8765`.
-   Price monitoring checks for a >2% increase compared to the earliest price within the last 60 seconds for each ticker.

## Task 3: Cloud Integration with AWS (`task3`)

This task simulates an AWS Lambda function analyzing trade data stored in a structure similar to S3.

### Components

-   `lambda_simulation.py`: The Python script simulating the Lambda function.
-   `simulated_s3/`: Directory simulating the input S3 bucket structure.
    -   `2025/06/05/trades.csv`: Sample input trade data.
-   `simulated_s3_output/`: Directory simulating the output S3 bucket location.

### Setup and Execution

1.  **Prerequisites:** Ensure Python 3.11+ is installed.
2.  **Unzip:** Extract the contents of `task3`.
3.  **Navigate:** Open a terminal in the extracted `task3_aws_lambda` directory.
4.  **Install Dependencies:**
    ```bash
    pip install pandas boto3
    ```
    *(Note: `boto3` is included conceptually as per the task description, but the simulation uses local file operations.)*
5.  **Run Simulation:**
    ```bash
    python3.11 lambda_simulation.py
    ```
    The script will:
    *   Simulate finding the `trades.csv` file for the target date (default: `2025-06-05`).
    *   Read the CSV using pandas.
    *   Calculate the total traded volume and average price per stock.
    *   Print the analysis results to the console.
    *   Save the analysis results to `simulated_s3_output/2025/06/05/analysis_2025-06-05.csv`.

### Assumptions

-   S3 interaction is simulated using local directories (`simulated_s3` and `simulated_s3_output`).
-   The target date for analysis is hardcoded as `2025-06-05` but can be overridden by setting the `TARGET_DATE` environment variable (e.g., `export TARGET_DATE='YYYY-MM-DD'`).
-   Input CSV file is expected to be named `trades.csv` within the date-based directory structure.

## Task 4: Algorithmic Trading Simulation (`task4`)

This task implements and simulates a simple Moving Average Crossover trading strategy.

### Components

-   `trading_simulation.py`: The Python script performing the simulation.
-   `historical_data.csv`: Sample historical stock price data (AAPL, partial 2023).
-   `data_with_signals.csv`: Output CSV containing the original data plus calculated moving averages and trading signals.
-   `simulation_report.txt`: Text file summarizing the simulation parameters, trade log, and performance.

### Setup and Execution

1.  **Prerequisites:** Ensure Python 3.11+ is installed.
2.  **Unzip:** Extract the contents of `task4`.
3.  **Navigate:** Open a terminal in the extracted `task4_trading_sim` directory.
4.  **Install Dependencies:**
    ```bash
    pip install pandas numpy
    ```
5.  **Run Simulation:**
    ```bash
    python3.11 trading_simulation.py
    ```
    The script will:
    *   Load data from `historical_data.csv`.
    *   Calculate the short-term (10-day) and long-term (30-day) moving averages.
    *   Generate buy/sell signals based on crossovers.
    *   Simulate trades starting with an initial capital of $10,000.
    *   Print performance summary to the console.
    *   Save the detailed report to `simulation_report.txt`.
    *   Save the data with calculated indicators and signals to `data_with_signals.csv`.

### Assumptions

-   Uses the provided `historical_data.csv`.
-   Moving average windows are set to 10 (short) and 30 (long) days within the script, chosen due to the limited sample data size. These can be easily modified in `trading_simulation.py`.
-   Initial capital is $10,000.
-   Trades are simulated based on the closing price of the day the signal occurs.
-   No transaction costs or slippage are considered in this simple simulation.


