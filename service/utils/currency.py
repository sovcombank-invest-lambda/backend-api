from worker.utils.rates import get_current_exchange_rates 
from service.schemas.exchange_rates import ExchangeRate 
from datetime import datetime
from sqlalchemy import insert, select, delete, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from service.configs.get_settings import get_fastapi_settings

from aiohttp import ClientSession

async def get_latest_currency(currency: str, session: AsyncSession) -> ExchangeRate:
    async with ClientSession() as session:
        response = await session.get(
            "https://api.apilayer.com/fixer/latest?base=RUB&symbols=EUR,USD,JPY,CNY",
            headers={
                'apikey': get_fastapi_settings().FIXERIO_API_KEY
            }
        )
        if not response.status == 200:
            raise InternalServerError(Exception("API KEY EXPIRED PROBABLY")) 
        data = await response.json()
        return ExchangeRate(
            code="1000",
            symbol=currency,
            amount=1,
            rate=data["rates"][currency],
            created_at=datetime.now()
        )

