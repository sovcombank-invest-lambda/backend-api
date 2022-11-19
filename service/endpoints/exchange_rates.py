
from uuid import UUID
from typing import List
from fastapi import APIRouter, Form, Body, Query
from fastapi.param_functions import Depends
from fastapi.security import OAuth2PasswordRequestForm
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession

from service.utils.auth import create_access_token, get_password_hash, verify_password, get_current_user
from service.exceptions.common import ForbiddenException 
from service.schemas.common import SuccessfullResponse, TokenOut
from migrations.connection.session import get_session
from service.services.auth import add_new_user, get_user
from service.services.currency_account import get_currency_accounts, create_currency_account, delete_currency_account, get_currencies, make_demo_transaction
from service.schemas.currency_account import CurrencyAccountIn, CurrencyAccountDelete, CurrencyAccountOut, Currency, CurrencyTransaction
from service.exceptions.common import ForbiddenException
from migrations.models.users import Users, Roles
from service.services.exchange_rates import get_exchange_rates
from service.schemas.exchange_rates import ExchangeRate


exchange_rates_router = APIRouter(tags=["Котировки"])

@exchange_rates_router.get("/exchange_rates", response_model=List[ExchangeRate])
async def get_exchange_rate(
    session: AsyncSession = Depends(get_session),
    start_date: datetime = Query(..., description='Дата начала'),
    end_date: datetime = Query(..., description='Дата конца')
) -> SuccessfullResponse:
    result = await get_exchange_rates(start_date, end_date, session)    
    return [ExchangeRate.from_orm(rate) for rate in result]

