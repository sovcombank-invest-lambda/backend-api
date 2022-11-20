
from uuid import UUID
from typing import List
from fastapi import APIRouter, Form, Body
from fastapi.param_functions import Depends
from fastapi.security import OAuth2PasswordRequestForm

from sqlalchemy.ext.asyncio import AsyncSession

from service.utils.auth import create_access_token, get_password_hash, verify_password, get_current_user
from service.exceptions.common import ForbiddenException 
from service.schemas.common import SuccessfullResponse, TokenOut
from migrations.connection.session import get_session
from service.services.auth import add_new_user, get_user
from service.services.currency_account import get_currency_accounts, create_currency_account, delete_currency_account, get_currencies, make_demo_transaction
from service.schemas.currency_account import CurrencyAccountIn, CurrencyTransfer, CurrencyAccountDelete, CurrencyAccountOut, Currency, CurrencyTransaction
from service.exceptions.common import ForbiddenException
from migrations.models.users import Users, Roles
from service.services.currency_account import transfer_currency_by_id
from service.services.statistics import get_transactions_for_user
from service.schemas.statistics import UserTransactions, Transaction
statistics_router = APIRouter(tags=["Статистические ручки"])

@statistics_router.get("/user/statistics", response_model=List[Transaction])
async def get_transactions_in_specified_period(phone: str = Depends(get_current_user),
                                               user_transactions: UserTransactions = Depends(),
                                               session: AsyncSession = Depends(get_session)
) -> List[Transaction]:
    user = await get_user(phone, session)
    data = await get_transactions_for_user(
        user.id,
        user_transactions.currency_account_id,
        user_transactions.start_date,
        user_transactions.end_date,
        session
    )
    return [Transaction(
        change_value=el[0],
        currency=el[2],
        created_at=el[1]
    ) for el in data]


