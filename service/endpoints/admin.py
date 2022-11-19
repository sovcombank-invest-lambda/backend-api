
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
from service.services.admin import change_user_role, get_users, get_transaction_for_user
from service.schemas.admin import UserOut

admin_router = APIRouter(tags=["Функционал админов"])

@admin_router.post("/admin/user/role", response_model=SuccessfullResponse)
async def change_role_of_user(phone: str = Depends(get_current_user),
                              change_user_role: ChangeUserRole = Depends()
                              session: AsyncSession = Depends(get_session)) -> None:
    user = await get_user(phone, session)
    if not user.role == Roles.ADMIN.value:
        raise ForbiddenException("User is not an admin")
    await change_user_role(change_user_role.user_id, change_user_role.new_role, session) 
    return SuccessfullResponse()

@admin_router.get("/admin/user", response_model=List[UserOut])
async def get_users(phone: str = Depends(get_current_user),
                    session: AsyncSession = Depends(get_session)) -> None:
    user = await get_user(phone, session)
    if not user.role == Roles.ADMIN.value:
        raise ForbiddenException("User")
    users = await get_users()
    return [UserOut.from_orm(user) for user in users]  


