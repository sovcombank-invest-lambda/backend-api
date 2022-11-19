from uuid import UUID
from datetime import datetime

from fastapi import Depends, File, UploadFile, Form
from pydantic import BaseModel, Field
from migrations.models.users import Gender, Users



class CurrencyAccountIn(BaseModel):
    currency_id: UUID = Field(..., description="UUID валюты")
    name: str = Field(..., description="Название валютного счета")
    
class CurrencyAccountOut(BaseModel):
    name: str = Field(..., description='Название валютного счета')
    created_at: datetime = Field(..., description='Дата создания')
    
class CurrencyAccountDelete(BaseModel):
    currency_account_id: UUID = Field(..., description="UUID валютного счета")
    