from uuid import UUID

from fastapi import Depends, File, UploadFile, Form
from pydantic import BaseModel, Field
from migrations.models.users import Gender, Users



class UserIn(BaseModel):
    email: str = Form(..., description="Почта пользователя")
    gender: Gender = Form(None, description="Пол пользователя")
    name: str = Form(None, description="Имя пользователя")
    surname: str = Form(None, description="Фамилия пользователя")
    

class SuccessfullResponse(BaseModel):
    details: str = Field("Выполнено", title="Статус операции")



class TokenOut(BaseModel):
    access_token: str = Field(..., description="Access token")
    token_type: str = Field(..., description="Token type")
