
from pydantic import BaseModel, Field, validator
from datetime import datetime
from typing import Literal, Optional

class TradeBase(BaseModel):
    ticker: str = Field(..., description="Stock ticker symbol")
    price: float = Field(..., gt=0, description="Trade price, must be positive")
    quantity: int = Field(..., gt=0, description="Trade quantity, must be positive")
    side: Literal['buy', 'sell'] = Field(..., description="Trade side: 'buy' or 'sell'")

class TradeCreate(TradeBase):
    pass

class Trade(TradeBase):
    id: int
    timestamp: datetime

    class Config:
        orm_mode = True

