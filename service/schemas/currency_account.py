from uuid import UUID
from datetime import datetime

from fastapi import Depends, File, UploadFile, Form
from pydantic import BaseModel, Field
from migrations.models.users import Gender, Users



class CurrencyAccountIn(BaseModel):
    currency_id: UUID = Field(..., description="UUID валюты")
    name: str = Field(..., description="Название валютного счета")
    
class CurrencyAccountOut(BaseModel):
    id: str = Field(..., description='UUID валютного счета')
    name: str = Field(..., description='Название валютного счета')
    value: float = Field(..., description='Состояние счета')
    currency_id: UUID = Field(..., description='UUID валютного счета')
    created_at: datetime = Field(..., description='Дата создания')
    class Config:
        orm_mode = True
    
class CurrencyAccountDelete(BaseModel):
    currency_account_id: UUID = Field(..., description="UUID валютного счета")
    
class Currency(BaseModel):
    id: UUID = Field(..., description='UUID валюты')
    name: str = Field(..., description='сокр. название валюты')
    fullname: str = Field(..., description='Полное название валюты')
    value: float = Field(..., description='Курс валюты')
    class Config:
        orm_mode = True
    
class CurrencyTransaction(BaseModel):
    change_value: float = Field(..., description="Изменение средств на счете")
    currency_account_id: UUID = Field(..., description="UUID валютного счета")
    