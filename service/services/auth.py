from sqlalchemy import insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from migrations.models.users import Users, Roles
from migrations.models.requests import Requests, RequestStatus, RequestTypes
from service.exceptions.common import BadRequest,NotFoundException
from service.schemas.auth import UserIn


async def add_new_user(login: str, hashed_password: str, session: AsyncSession) -> None:
    try:
        query = insert(Users).values(
            phone=login,
            hashed_password=hashed_password
            # **({'gender': user_in.gender} if user_in.gender else {}),
            # **({'name': user_in.name} if user_in.name else {}),
            # **({'surname': user_in.surname} if user_in.surname else {}),
        )
        await session.execute(query)
        await session.commit()
    except IntegrityError as e:
        raise BadRequest("User already exist", e) from e

async def get_user(login: str, session: AsyncSession) -> Users:
    query = select(Users).where(
        Users.phone == login
    )
    result = (await session.execute(query)).scalars().first()
    if not result:
        raise NotFoundException("User not found")
    return result

async def add_task_for_verification(phone: str, session: AsyncSession) -> None:
    user = await get_user(phone, session)
    query = insert(Requests).values(
        request_type=RequestTypes.REGISTRATION,
        request_status=RequestStatus.PENDING,
        creator_id=user.id
    )
    try:
        await session.execute(query)
        await session.commit()
    except IntegrittyError as e:
        await session.rollback()

