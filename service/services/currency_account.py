from uuid import UUID
from typing import List

from sqlalchemy import insert, select, delete, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from migrations.models.currency_account import CurrencyAccount
from service.exceptions.common import BadRequest,NotFoundException
from service.schemas.auth import UserIn
from migrations.models.currency import Currency
from migrations.models.transactions import Transactions

async def create_currency_account(name: str, currency_id: UUID, user_id: UUID, session: AsyncSession) -> None:
    try:
        query = insert(CurrencyAccount).values(
            name=name,
            currency_id=str(currency_id),
            user_id=str(user_id)
        )
        await session.execute(query)
        await session.commit()
    except IntegrityError as e:
        raise NotFoundException("User/Currency not found") from e

async def get_currency_accounts(user_id: UUID, session: AsyncSession) -> List[CurrencyAccount]:
    query = select(CurrencyAccount).where(
        CurrencyAccount.user_id == str(user_id)
    )
    result = (await session.execute(query)).scalars().all()
    if not result:
        return []
    return result

async def delete_currency_account(currency_account_id: UUID, user_id: UUID, session: AsyncSession) -> None:
    try:
        query = delete(CurrencyAccount).where(
            CurrencyAccount.user_id == str(user_id),
            CurrencyAccount.id == str(currency_account_id)
        )
        await session.execute(query)
        await session.commit()
    except IntegrityError as e:
        raise NotFoundException("User/Currency not found") from e
    
async def get_currencies(session: AsyncSession) -> List[Currency]:
    query = select(Currency)
    result = (await session.execute(query)).scalars().all()
    return result

async def make_demo_transaction(change_value: float, user_id: UUID, currency_account_id: UUID, session: AsyncSession) -> None:
    query = select(CurrencyAccount).where(
        CurrencyAccount.id ==str( currency_account_id),
        CurrencyAccount.user_id == str(user_id)
    )
    result = (await session.execute(query)).scalars().first()
    query1 = update(CurrencyAccount).values(
        value=result.value+change_value
    ).where(
        CurrencyAccount.id ==str(currency_account_id),
        CurrencyAccount.user_id == str(user_id)
    )
    query2 = insert(Transactions).values(
        currency_account_id = currency_account_id,
        change_value = change_value
    )
    try:
        await session.execute(query1)
        await session.execute(query2)
        await session.commit()
    except IntegrityError as e:
        raise NotFoundException("Currency account not found") from e