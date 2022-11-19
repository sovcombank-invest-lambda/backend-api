import asyncio
from datetime import datetime
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

def get_current_exchange_rates(exchange_rates: List[str], today: datetime = datetime.now()) -> List[ExchangeRate]:
    formatted_time = f'{today.day:02}.{today.month:02}.{today.year}'
    results = get_exchange_rates(formatted_time, symbols=exchange_rates)
    results = [ExchangeRate(**rate) for rate in results]
    return results

async def upload_new_data(new_rates: List[ExchangeRate]) -> None:
    async for session in get_session():
        queries = [ 
            insert(ExchangeRates).values(
                code=rate.code,
                symbol=rate.symbol,
                amount=rate.amount,
                rate=rate.rate
            )
            for rate in new_rates
        ]
        coroutines = [session.execute(query) for query in queries]
        await asyncio.gather(*coroutines)
        await session.commit()
    
