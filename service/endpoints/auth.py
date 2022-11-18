from uuid import UUID
from fastapi import APIRouter, Form, Body
from fastapi.param_functions import Depends
from fastapi.security import OAuth2PasswordRequestForm

from sqlalchemy.ext.asyncio import AsyncSession

from service.utils.auth import create_access_token, get_password_hash, verify_password, get_current_user
from service.exceptions.common import ForbiddenException 
from service.schemas.common import SuccessfullResponse, TokenOut, JobsOut
from migrations.connection.session import get_session
from service.services.auth import add_new_user, get_user, get_jobs, update_user_job

auth_router = APIRouter(tags=["Аутентификация"])


@auth_router.post("/user/register", response_model=SuccessfullResponse)
async def user_register(
    request: OAuth2PasswordRequestForm = Depends(),
    session: AsyncSession = Depends(get_session)
) -> SuccessfullResponse:
    request.password = get_password_hash(request.password)
    await add_new_user(request.username, request.password, session)
    return SuccessfullResponse()


@auth_router.post("/user/login", response_model=TokenOut)
async def user_login(request: OAuth2PasswordRequestForm = Depends(),
                     session: AsyncSession = Depends(get_session)) -> TokenOut:
    user = await get_user(request.username, session)
    if not verify_password(request.password, user.password):
        raise ForbiddenException("Wrong password")
    access_token = create_access_token(data={"sub": user.username})
    token = TokenOut(access_token=access_token, token_type="bearer")
    return token
