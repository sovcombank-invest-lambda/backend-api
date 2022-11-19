
from uuid import UUID
from typing import List
from datetime import datetime
from sqlalchemy import insert, select, delete, update, and_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from migrations.models.currency_account import CurrencyAccount
from service.exceptions.common import BadRequest,NotFoundException
from service.schemas.auth import UserIn
from migrations.models.currency import Currency
from migrations.models.transactions import Transactions
from migrations.models.exchange_rates import ExchangeRates

async def get_exchange_rates(start_date: datetime, end_date: datetime, session: AsyncSession) -> List[ExchangeRates]: 
    query = select(ExchangeRates).where(
        and_(
            ExchangeRates.created_at >= start_date,
            ExchangeRates.created_at <= end_date
        )
    )
    results = (await session.execute(query)).scalars().all()
    if not results:
        return []
    return results
