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
from migrations.models.users import Users, Roles
from migrations.models.requests import RequestStatus, Requests, RequestTypes

async def change_user_role_by_id(user_id: UUID, new_role: Roles, session: AsyncSession) -> None:
    query = update(Users).values(
        role = new_role
    ).where(
        Users.id == str(user_id )
    )
    await session.execute(query)
    await session.commit()

async def get_userss(session: AsyncSession) -> List:
    print(session)
    query = select(Users)
    result = (await session.execute(query)).scalars().all()
    return result

async def get_pending_registration_statuses(session: AsyncSession) -> List[Requests]:
    query = select(Requests).where(
        Requests.request_type == RequestTypes.REGISTRATION,
        Requests.request_status == RequestStatus.PENDING
    )
    results = (await session.execute(query)).scalars().all()
    return results

async def change_user_registration_status(user_id: UUID,
                                          status: RequestStatus,
                                          session: AsyncSession
                                          ) -> None:
    query = update(Requests).values(
        request_status = status
    ).where(
        Requests.creator_id == str(user_id),
        Requests.request_type == RequestTypes.REGISTRATION,
        Requests.request_status == RequestStatus.PENDING
    )
    try:
        await session.execute(query)
        await session.commit()
    except IntegrityError as e:
        await session.rollback()
