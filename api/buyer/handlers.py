from uuid import uuid4

from fastapi import (
    APIRouter,
    status,
    UploadFile,
    File,
    Body,
    HTTPException,
)

from api.buyer.crud import BuyerCrud
from api.buyer.schemas import BuyerShow, BuyerCreate
from api.buyer.yandex_client import yandex_client

router = APIRouter(tags=["Buyer"], prefix="/buyer")


@router.post("/", response_model=BuyerShow, status_code=status.HTTP_201_CREATED)
async def create_user(
    buyer_in: BuyerCreate = Body(...), photo: UploadFile = File(...)
) -> BuyerShow:
    buyer_id = uuid4()

    url_for_upload = await yandex_client.get_url_for_upload(
        id=buyer_id, name=buyer_in.name, surname=buyer_in.surname, file=photo
    )
    if url_for_upload is False:
        raise HTTPException(status_code=503, detail="Ошибка при сохранении фотографии")

    photo_url = await yandex_client.upload_photo(url=url_for_upload, file=photo)
    if photo is False:
        raise HTTPException(status_code=503, detail="Ошибка при сохранении фотографии")

    photo_url_for_db = f"{buyer_id}_{buyer_in.name}_{buyer_in.surname}_{photo_url}"

    buyer = await BuyerCrud.create_buyer(
        buyer_in=buyer_in,
        buyer_id=buyer_id,
        photo_url=photo_url_for_db,
    )
    return BuyerShow(
        id=buyer.id,
        name=buyer.name,
        surname=buyer.surname,
        patronymic=buyer.patronymic,
        date_of_birth=buyer.date_of_birth,
        sex=buyer.sex,
        photo=buyer.photo,
        personal_data_processing=buyer.personal_data_processing,
    )
