
from uuid import UUID
from typing import List
from fastapi import APIRouter, Form, Body
from fastapi.param_functions import Depends
from fastapi.security import OAuth2PasswordRequestForm

from sqlalchemy.ext.asyncio import AsyncSession

from service.utils.auth import create_access_token, get_password_hash, verify_password, get_current_user
from service.exceptions.common import ForbiddenException 
from service.schemas.common import SuccessfullResponse, TokenOut
from migrations.connection.session import get_session
from service.services.auth import add_new_user, get_user
from service.services.currency_account import get_currency_accounts, create_currency_account, delete_currency_account, get_currencies, make_demo_transaction
from service.schemas.currency_account import CurrencyAccountIn, CurrencyTransfer, CurrencyAccountDelete, CurrencyAccountOut, Currency, CurrencyTransaction
from service.exceptions.common import ForbiddenException
from migrations.models.users import Users, Roles
from service.services.currency_account import transfer_currency_by_id
from service.schemas.prediction import PredictedPriceChange
from service.utils.predict import clean_text, news_to_int, padding_news, unnormalize, predict
import numpy as np

predict_router = APIRouter(tags=["Функционал предсказаний"])

@predict_router.post("/predict", response_model=PredictedPriceChange)
async def predicts_currence_change(
    currency_id: UUID = Body(..., description = "UUID валюты"),
    news_body: str = Body(..., description="Тело новости"),
    session: AsyncSession = Depends(get_session)
) -> PredictedPriceChange :
    clean_news = clean_text(news_body)
    int_news = news_to_int(clean_news)
    pad_news = padding_news(int_news)
    pad_news = np.array(pad_news).reshape((1,-1))
    pred = predict([pad_news, pad_news])
    #pred = model.predict([pad_news,pad_news])
    price_change = unnormalize(pred)
    return PredictedPriceChange(
        result=price_change
    ) 
