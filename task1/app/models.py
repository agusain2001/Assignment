
from sqlalchemy import Column, Integer, String, Float, DateTime, Enum
from sqlalchemy.sql import func
from .database import Base
import enum

class TradeSide(str, enum.Enum):
    BUY = "buy"
    SELL = "sell"

class Trade(Base):
    __tablename__ = "trades"

    id = Column(Integer, primary_key=True, index=True)
    ticker = Column(String, index=True, nullable=False)
    price = Column(Float, nullable=False)
    quantity = Column(Integer, nullable=False)
    side = Column(Enum(TradeSide), nullable=False)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())

