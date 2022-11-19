from uuid import UUID
from typing import List
from datetime import datetime
from sqlalchemy import insert, select, delete, update, and_, in_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from migrations.models.currency_account import CurrencyAccount
from service.exceptions.common import BadRequest,NotFoundException
from service.schemas.auth import UserIn
from migrations.models.currency import Currency
from migrations.models.transactions import Transactions
from migrations.models.exchange_rates import ExchangeRates
from migrations.models.users import Users, Roles

async def change_user_role(user_id: UUID, new_role: Roles, session: AsyncSession) -> None:
    query = update(Users).values(
        role = new_role
    ).where(
        Users.id == user_id 
    )
    await session.execute(query)
    await session.commit()

async def get_users() -> List:
    query = select(Users)
    result = (await session.execute(query)).scalars().all()
    return result

async def get_transaction_for_user(user_id: UUID, start_date: datetime, end_date: datetime) -> List[Transactions]:
    query = select(Transactions).where(
        and_(
            Transactions.created_at >= start_date,
            Transactions.created_at <= end_date,
            Transactions.currency_account_id.in_(select(CurrencyAccount).where(
                CurrencyAccount.user_id == user_id
            ))
        ) 
    )
    result = (await session.execute(query)).scalars().all()
    return result
