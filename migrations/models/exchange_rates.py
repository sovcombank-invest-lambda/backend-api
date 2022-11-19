import uuid
from datetime import datetime
from enum import Enum

from sqlalchemy import Boolean, INTEGER, Column, String, TIMESTAMP, Float, ForeignKey, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID, TSVECTOR, ENUM

from migrations.models.users import Users
from migrations.models.currency import Currency

from pytz import UTC

from migrations.migrator.base import DeclarativeBase


class ExchangeRates(DeclarativeBase):
    __tablename__ = "exchange_rates"

    id = Column(UUID, unique=True, primary_key=True, default=lambda: str(uuid.uuid4()))
    code = Column(INTEGER, nullable=False)
    symbol = Column(String, nullable=False)
    amount = Column(INTEGER, nullable=False)
    rate = Column(Float, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, default = lambda x: datetime.now(UTC))
    
