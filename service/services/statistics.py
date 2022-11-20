
from uuid import UUID
from typing import List
from datetime import datetime
from sqlalchemy import insert, select, delete, update, and_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from migrations.models.transactions import Transactions
from migrations.models.currency import Currency
from migrations.models.currency_account import CurrencyAccount

async def get_transactions_for_user(user_id: UUID, 
                                    currency_account_id: UUID,
                                    start_date: datetime, 
                                    end_date: datetime,
                                    session: AsyncSession) -> List[tuple[str,datetime,str]]:
    query = select([
        Transactions.change_value,
        Transactions.created_at,
        Currency.name
    ]).join(CurrencyAccount, 
        Transactions.currency_account_id == CurrencyAccount.id
    ).join(Currency,
        Currency.id == CurrencyAccount.currency_id
    ).where(
        and_(
            Transactions.created_at >= start_date,
            Transactions.created_at <= end_date,
            Transactions.currency_account_id == str(currency_account_id),
            CurrencyAccount.user_id == str(user_id)
        )
    ).order_by(Transactions.created_at)

    result = (await session.execute(query)).all()
    print(result)
    return result
