import uuid
from datetime import datetime
from enum import Enum

from sqlalchemy import Boolean, Column, String, TIMESTAMP, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, TSVECTOR, ENUM

from pytz import UTC

from migrations.migrator.base import DeclarativeBase
from migrations.models.users import Users

class RequestTypes(Enum):
    REGISTRATION: str = "REGISTRATION"
    USER_TRANSACTIONS: str = "USER_TRANSACTIONS"
    ADMIN_TRANSACTIONS: str = "ADMIN_TRANSACTIONS"

class RequestStatus(Enum):
    PENDING: str = "PENDING"
    FULLFILLED: str = "FULLFILLED"
    CANCELED: str = "CANCELED"


class Requests(DeclarativeBase):
    __tablename__ = "requests"

    id = Column(UUID, unique=True, primary_key=True, default=lambda: str(uuid.uuid4()))
    request_type = Column(ENUM(RequestTypes), nullable=False)
    request_status = Column(ENUM(RequestStatus), nullable=False)
    response = Column(String, nullable=True)
    creator_id = Column(UUID, ForeignKey(Users.id, ondelete="CASCADE"), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, default = lambda x: datetime.now(UTC))
