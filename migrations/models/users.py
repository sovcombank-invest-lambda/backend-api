import uuid
from datetime import datetime
from enum import Enum

from sqlalchemy import Boolean, Column, String, TIMESTAMP
from sqlalchemy.dialects.postgresql import UUID, TSVECTOR, ENUM

from pytz import UTC

from migrations.migrator.base import DeclarativeBase

class Roles(Enum):
    DEMO: str = "DEMO"
    UNVERIFIED: str = "UNVERIFIED"
    REGULAR: str = "REGULAR"
    ADMIN: str = "ADMIN"

class Gender(Enum):
    MALE: str = "MALE"
    FEMALE: str = "FEMALE"
    UNSPECIFIED: str = "UNSPECIFIED"

class Users(DeclarativeBase):
    __tablename__ = "users"

    id = Column(UUID, unique=True, primary_key=True, default=lambda: str(uuid.uuid4()))
    role = Column(ENUM(Roles), nullable=False, default=Roles.DEMO)
    name = Column(String, nullable=True)
    surname = Column(String, nullable=True)
    gender = Column(ENUM(Gender), nullable=False, default=Gender.UNSPECIFIED)
    phone = Column(String, nullable=False, unique=True)
    hashed_password = Column(String, nullable=False)
    avatar_id = Column(String, nullable=True)
    birth_date = Column(TIMESTAMP(timezone=True), nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, default = lambda x: datetime.now(UTC))