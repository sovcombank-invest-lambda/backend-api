from pydantic import Field,BaseModel
from uuid import UUID
from fastapi import Query
from datetime import datetime

class Transaction(BaseModel):
    change_value: float = Field(..., description="Величина притока/убытка денежных средств")
    currency: str = Field(..., description="Наименование валюты")
    created_at: datetime = Field(..., description="Дата проведения транзакции")

class UserTransactions(BaseModel):
    start_date: datetime = Query(..., description="Начало промежуутка сканирования")
    end_date: datetime = Query(..., description="Конце промежутка сканирования")
    currency_account_id: UUID = Query(..., description="UUID валютного счета")
