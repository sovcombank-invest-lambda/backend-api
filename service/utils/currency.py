from worker.utils.rates import get_current_exchange_rates 
from service.schemas.exchange_rates import ExchangeRate 
from migrations.models.exchange_rates import ExchangeRates

from sqlalchemy import insert, select, delete, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

async def get_latest_currency(currency: str, session: AsyncSession) -> ExchangeRates:
    query = select(ExchangeRates).where(
        ExchangeRates.symbol == currency
    ).order_by(ExchangeRates.created_at.desc()).limit(1)
    result = (await session.execute(query)).scalars().first()
    return result
