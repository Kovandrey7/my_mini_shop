from uuid import UUID

from api.buyer.schemas import BuyerCreate
from database.db_helper import db_helper
from database.models import Buyer


class BuyerCrud:
    @classmethod
    async def create_buyer(
        cls, buyer_in: BuyerCreate, buyer_id: UUID, photo_url: str
    ) -> Buyer:
        async with db_helper.session_factory() as session:
            new_buyer = Buyer(
                id=buyer_id,
                name=buyer_in.name,
                surname=buyer_in.surname,
                patronymic=buyer_in.patronymic,
                date_of_birth=buyer_in.date_of_birth,
                sex=buyer_in.sex,
                photo=photo_url,
                personal_data_processing=buyer_in.personal_data_processing,
            )
            session.add(new_buyer)
            await session.commit()
            return new_buyer
