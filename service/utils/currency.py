from worker.utils.rates import get_current_exchange_rates 
from service.schemas.exchange_rates import ExchangeRate 
from migrations.models.exchane_rates import ExchangeRates

async def get_latest_currency(currency: str) -> ExchangeRates:
    query = select(EchangeRates).where(
        ExchangeRates.symbol == currency
    ).order_by(EchangeRates.created_at.desc()).limit(1)
    result = (await session.execute(query)).scalars().first()
    return result
