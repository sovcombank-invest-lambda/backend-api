import uuid
from datetime import datetime
from enum import Enum

from sqlalchemy import Boolean, Column, String, TIMESTAMP, ForeignKey, FLOAT
from sqlalchemy.dialects.postgresql import UUID, TSVECTOR, ENUM

from pytz import UTC
from migrations.models.currency import Currency

from migrator.base import DeclarativeBase


class Transactions(DeclarativeBase):
    __tablename__ = "transactions"

    id = Column(UUID, unique=True, primary_key=True, default=lambda: str(uuid.uuid4()))
    currency_account_id = Column(UUID, ForeignKey(Currency.id, ondelete="CASCADE"), nullable=False)
    change_value = Column(FLOAT, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, default = lambda x: datetime.now(UTC))