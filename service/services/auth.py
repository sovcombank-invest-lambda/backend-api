from sqlalchemy import insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from migrations.models.users import Users
from service.exceptions.common import BadRequest,NotFoundException
from service.schemas.auth import UserIn


async def add_new_user(login: str, hashed_password: str, user_in: UserIn, session: AsyncSession) -> None:
    try:
        query = insert(Users).values(
            username=login,
            email=user_in.email,
            hashed_password=hashed_password,
            **({'gender': user_in.gender} if user_in.gender else {}),
            **({'name': user_in.name} if user_in.name else {}),
            **({'surname': user_in.surname} if user_in.surname else {}),
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
