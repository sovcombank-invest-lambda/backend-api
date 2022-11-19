
from uuid import UUID
from datetime import datetime

from fastapi import Depends, File, UploadFile, Form
from pydantic import BaseModel, Field
from migrations.models.users import Gender, Users

class ExchangeRate(BaseModel):
    code: int
    symbol: str
    amount: int
    rate: float
    created_at: datetime
    
    class Config:
        orm_mode = True

