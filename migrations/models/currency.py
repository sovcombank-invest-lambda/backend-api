import uuid
from datetime import datetime
from enum import Enum

from sqlalchemy import Boolean, Column, String, TIMESTAMP, Float
from sqlalchemy.dialects.postgresql import UUID, TSVECTOR, ENUM

from pytz import UTC

from migrations.migrator.base import DeclarativeBase


class Currency(DeclarativeBase):
    __tablename__ = "currency"

    id = Column(UUID, unique=True, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, nullable=False, unique=True)
    fullname = Column(String, nullable=True)
    value = Column(Float, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, default = lambda x: datetime.now(UTC))