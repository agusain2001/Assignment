
from sqlalchemy.orm import Session
from . import models, schemas
from datetime import datetime
from typing import List, Optional

def create_trade(db: Session, trade: schemas.TradeCreate) -> models.Trade:
    db_trade = models.Trade(**trade.dict())
    db.add(db_trade)
    db.commit()
    db.refresh(db_trade)
    return db_trade

def get_trades(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    ticker: Optional[str] = None,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None
) -> List[models.Trade]:
    query = db.query(models.Trade)
    if ticker:
        query = query.filter(models.Trade.ticker == ticker)
    if start_date:
        query = query.filter(models.Trade.timestamp >= start_date)
    if end_date:
        query = query.filter(models.Trade.timestamp <= end_date)
    return query.offset(skip).limit(limit).all()

