from uuid import UUID

from sqlalchemy import insert, select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from migrations.models.currency_account import CurrencyAccount
from service.exceptions.common import BadRequest,NotFoundException
from service.schemas.auth import UserIn

async def create_currency_account(name: str, currency_id: UUID, user_id: UUID, session: AsyncSession) -> None:
    try:
        query = insert(CurrencyAccount).values(
            name=name,
            currency_id=currency_id,
            user_id=user_id
        )
        await session.execute(query)
        await session.commit()
    except IntegrityError as e:
        raise NotFoundException("User/Currency not found")

async def get_currency_accounts(user_id: UUID, session: AsyncSession) -> list[CurrencyAccount]:
    query = select(CurrencyAccount).where(
        CurrencyAccount.user_id == user_id
    )
    result = (await session.execute(query)).scalars().all()
    if not result:
        return []
    return result

async def delete_currency_account(currency_account_id: UUID, user_id: UUID, session: AsyncSession) -> None:
    try:
        query = delete(CurrencyAccount).where(
            CurrencyAccount.user_id == user_id,
            CurrencyAccount.id == currency_account_id
        )
        await session.execute(query)
        await session.commit()
    except IntegrityError as e:
        raise NotFoundException("User/Currency not found")