from sqlalchemy import insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from migrations.models.users import Users
from service.exceptions.common import BadRequest,NotFoundException
from service.schemas.common import JobsOut


async def add_new_user(login: str, hashed_password: str, session: AsyncSession) -> None:
    try:
        query = insert(Users).values(
            username=login,
            password=hashed_password,
        )
        await session.execute(query)
        await session.commit()
    except IntegrityError as e:
        raise BadRequest("User already exist", e) from e
async def get_user(login: str, session: AsyncSession) -> Users:
    query = select(Users).where(
        Users.username == login
    )
    result = (await session.execute(query)).scalars().first()
    if not result:
        raise NotFoundException("User not found")
    return result
