
from uuid import UUID

from fastapi import Depends, File, UploadFile
from pydantic import BaseModel, Field


class PredictedPriceChange(BaseModel):
    result: float = Field("0.5", description="Предсказываемое изменение цены")
