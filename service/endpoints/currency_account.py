from uuid import UUID
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
from service.schemas.currency_account import CurrencyAccountIn, CurrencyAccountDelete, CurrencyAccountOut, Currency, CurrencyTransaction
from migrations.models.users import Users

currency_account_router = APIRouter(tags=["Валютный счет"])

@currency_account_router.get("/user/account", response_model=list[CurrencyAccountOut])
async def account_get(
    username: str = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
) -> SuccessfullResponse:
    user = await get_user(username, session)
    accounts = await get_currency_accounts(user.id, session)
    return [CurrencyAccountOut.from_orm(account) for account in accounts]

@currency_account_router.post("/user/account", response_model=SuccessfullResponse)
async def account_create(
    currency_account: CurrencyAccountIn = Depends(),
    username: str = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
) -> SuccessfullResponse:
    user = await get_user(username, session)
    await delete_currency_account(currency_account, user.id, session)
    return SuccessfullResponse()


@currency_account_router.delete("/user/account", response_model=SuccessfullResponse)
async def account_delete(
        currency_account_delete: CurrencyAccountDelete = Depends(),
        username: str = Depends(get_current_user),
        session: AsyncSession = Depends(get_session)) -> SuccessfullResponse:
    user = await get_user(username, session)
    await delete_currency_account(currency_account_delete.currency_account_id, user.id, session)
    return SuccessfullResponse()

@currency_account_router.get("/currency", response_model=list[Currency])
async def get_available_currencies(
    session: AsyncSession = Depends(get_session)
) -> SuccessfullResponse:
    currencies = await get_currencies(session)
    return [Currency.from_orm(currency) for currency in currencies]

@currency_account_router.post("/user/account/currency", response_model=SuccessfullResponse)
async def account_get(
    username: str = Depends(get_current_user),
    currency_transaction: CurrencyTransaction = Depends(),
    session: AsyncSession = Depends(get_session)
) -> SuccessfullResponse:
    user = await get_user(username, session)
    await make_demo_transaction(currency_transaction.change_value, user.id, currency_transaction.currency_account_id)
    return SuccessfullResponse()

