import json
import re
from datetime import date
from typing import Literal
from uuid import UUID

from fastapi import HTTPException
from pydantic import BaseModel, Field, model_validator, field_validator

LETTER_MATCH_PATTERN = re.compile(r"^[а-яА-Яa-zA-Z\-]+$")


class BuyerCreate(BaseModel):
    name: str = Field(examples=["Andrey"])
    surname: str = Field(examples=["Koval"])
    patronymic: str | None = Field(None, examples=["Dmitrievich"])
    date_of_birth: date = Field(..., examples=["2024-04-24"])
    sex: Literal["male", "female"] = Field("male", examples=["male", "female"])
    personal_data_processing: bool = Field(default=True)

    @model_validator(mode="before")
    @classmethod
    def validate_to_json(cls, value):
        if isinstance(value, str):
            return cls(**json.loads(value))
        return value

    @field_validator("name")
    def validate_name(cls, value):
        if not LETTER_MATCH_PATTERN.match(value):
            raise HTTPException(
                status_code=422, detail="Name should contains only letters"
            )
        return value

    @field_validator("surname")
    def validate_surname(cls, value):
        if not LETTER_MATCH_PATTERN.match(value):
            raise HTTPException(
                status_code=422, detail="Surname should contains only letters"
            )
        return value

    @field_validator("patronymic")
    def validate_patronymic(cls, value):
        if not LETTER_MATCH_PATTERN.match(value):
            raise HTTPException(
                status_code=422, detail="patronymic should contains only letters"
            )
        return value


class BuyerShow(BaseModel):
    id: UUID
    name: str
    surname: str
    patronymic: str
    date_of_birth: date
    sex: Literal["male", "female"]
    photo: str
    personal_data_processing: bool
