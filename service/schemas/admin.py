

from uuid import UUID
from datetime import datetime

from fastapi import Depends, Query, File, UploadFile, Form
from pydantic import BaseModel, Field
from migrations.models.users import Gender, Users, Roles

class ChangeUserRole(BaseModel):
    user_id: UUID = Field(..., description="UUID исследуемого пользователя")
    new_role: Roles = Field(..., description="Новая роль у пользователя")

class UserOut(BaseModel):
    id: UUID = Field(..., description="UUID пользователя")
    phone: str = Field(..., description="Номер телефона")
    class Config:
        orm_mode = true
