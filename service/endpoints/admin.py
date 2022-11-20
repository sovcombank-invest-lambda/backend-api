from typing import List
from uuid import UUID
from fastapi import APIRouter, Form, Body
from fastapi.param_functions import Depends
from fastapi.security import OAuth2PasswordRequestForm

from sqlalchemy.ext.asyncio import AsyncSession

from service.utils.auth import create_access_token, get_password_hash, verify_password, get_current_user
from service.exceptions.common import ForbiddenException 
from service.schemas.common import SuccessfullResponse, TokenOut
from migrations.connection.session import get_session
from service.services.auth import add_new_user, get_user
from service.schemas.auth import UserIn
from migrations.models.users import Users, Roles
from service.services.admin import change_user_role_by_id, get_userss, change_user_registration_status, get_pending_registration_statuses
from service.schemas.admin import UserOut
from service.schemas.admin import RequestOut, ChangeUserRole
from migrations.models.requests import RequestStatus 

admin_router = APIRouter(tags=["Функционал админов"])

@admin_router.post("/admin/user/role", response_model=SuccessfullResponse)
async def change_role_of_user(phone: str = Depends(get_current_user),
                              change_user_role: ChangeUserRole = Depends(),
                              session: AsyncSession = Depends(get_session)) -> None:
    user = await get_user(phone, session)
    if not user.role == Roles.ADMIN:
        raise ForbiddenException("User is not an admin")
    await change_user_role_by_id(change_user_role.user_id, change_user_role.new_role, session) 
    return SuccessfullResponse()

@admin_router.get("/admin/user", response_model=List[UserOut])
async def get_users(phone: str = Depends(get_current_user),
                    session: AsyncSession = Depends(get_session),
                    session2: AsyncSession = Depends(get_session)) -> None:
    user = await get_user(phone, session)
    if not user.role == Roles.ADMIN:
        raise ForbiddenException("User is not and Admin")
    users = await get_userss(session2)
    return [UserOut.from_orm(user) for user in users]  

@admin_router.get("/admin/requests", response_model=List[RequestOut])
async def get_pending_registration_requests(phone: str = Depends(get_current_user),
                                            session: AsyncSession = Depends(get_session)) -> None:
    user = await get_user(phone, session)
    if not user.role == Roles.ADMIN:
        raise ForbiddenException("User is not an Admin")
    requests = await get_pending_registration_statuses(session)
    return [
        RequestOut(
            created_at=el.created_at,
            creator_id=el.creator_id
        )
        for el in requests
    ]

@admin_router.post("/admin/requests", response_model=SuccessfullResponse)
async def change_registration_status(phone: str = Depends(get_current_user),
                                     user_id: UUID = Body(..., description='UUID пользвателя'),
                                     status: RequestStatus = Body(...),
                                     session: AsyncSession = Depends(get_session)
    ) -> None:
    user = await get_user(phone, session)
    if not user.role == Roles.ADMIN:
        raise ForbiddenException("User is not an Admin")
    await change_user_registration_status(user_id, status, session)
    return SuccessfullResponse()
