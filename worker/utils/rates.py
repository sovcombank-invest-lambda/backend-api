import asyncio
from typing import List
from cbr import get_exchange_rates
from pydantic import BaseModel
from migrations.connection.session import get_session
from migrations.models.exchange_rates import ExchangeRates
from sqlalchemy import insert

class ExchangeRate(BaseModel):
    code: int
    symbol: str
    amount: int
    rate: float

def get_current_exchange_rates(exchange_rates: List[str]) -> List[ExchangeRate]:
    today = datetime.now()
    formatted_time = f'{today.day:02}.{today.month:02}.{today.year}'
    results = get_current_exchange_rates(formatted_time, exchange_rates)
    results = [ExchangeRate(**rate) for rate in rates]
    return results

async def upload_new_data(new_rates: List[ExchangeRate]) -> None:
    async for session in get_session():
        queries = [ 
            query = insert(ExchangeRates).values(
                code=rate.code,
                symbol=rate.symbol,
                amount=rate.amount,
                rate=rate.rate
            )
            for rate in rates
        ]
        coroutines = [session.execute(query) for query in queries]
        await asyncio.gather(*coroutines)
        await session.execute()
    
