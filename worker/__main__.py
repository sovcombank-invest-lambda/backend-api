import asyncio
from worker.utils.rates import get_current_exchange_rates,upload_new_data 

async def main() -> None:
    rates = get_current_exchange_rates(["USD", "EUR", "JPY", "CNY"])
    await upload_new_data(rates)

asyncio.run(main())
