from datetime import datetime, date
from uuid import UUID

from sqlalchemy import Integer, Boolean, func
from sqlalchemy.orm import Mapped, mapped_column

from database.models.base import Base


class Buyer(Base):
    id: Mapped[UUID] = mapped_column(primary_key=True)
    name: Mapped[str]
    surname: Mapped[str]
    patronymic: Mapped[str | None]
    date_of_birth: Mapped[date]
    sex: Mapped[str]
    photo: Mapped[str | None]
    registration_date: Mapped[datetime] = mapped_column(
        server_default=func.now(), default=datetime.now
    )
    personal_data_processing: Mapped[bool] = mapped_column(Boolean, default=True)
