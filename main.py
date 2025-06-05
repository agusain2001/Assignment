
from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime

from . import crud, models, schemas
from .database import SessionLocal, engine, get_db

# Create database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Trading System API",
    description="API for managing trade operations as part of the Internship Assignment.",
    version="1.0.0"
)

@app.post("/trades/", response_model=schemas.Trade, status_code=201)
def create_trade_endpoint(trade: schemas.TradeCreate, db: Session = Depends(get_db)):
    """
    Record a new trade.

    - **ticker**: Stock ticker symbol (e.g., AAPL)
    - **price**: Trade price (must be > 0)
    - **quantity**: Trade quantity (must be > 0)
    - **side**: Trade side ("buy" or "sell")
    """
    # Basic validation is handled by Pydantic models
    # Additional validation could be added here (e.g., check if ticker exists)
    return crud.create_trade(db=db, trade=trade)

@app.get("/trades/", response_model=List[schemas.Trade])
def read_trades_endpoint(
    skip: int = 0,
    limit: int = 100,
    ticker: Optional[str] = Query(None, description="Filter trades by ticker symbol"),
    start_date: Optional[datetime] = Query(None, description="Filter trades from this date/time onwards (ISO format)"),
    end_date: Optional[datetime] = Query(None, description="Filter trades up to this date/time (ISO format)"),
    db: Session = Depends(get_db)
):
    """
    Retrieve a list of trades, with optional filtering by ticker and date range.
    """
    trades = crud.get_trades(
        db=db,
        skip=skip,
        limit=limit,
        ticker=ticker,
        start_date=start_date,
        end_date=end_date
    )
    return trades

# Add a root endpoint for basic check
@app.get("/")
def read_root():
    return {"message": "Welcome to the Trading System API"}


