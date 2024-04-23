from uuid import UUID

import aiohttp
from fastapi import UploadFile

from settings import settings


class YandexClient:
    def __init__(self):
        self.token_yadisk = settings.YANDEX_TOKEN
        self.url = "https://cloud-api.yandex.net/v1/disk/"

    def get_headers_ya_disk(self):
        return {
            "Content-Type": "application/json",
            "Authorization": f"OAuth {self.token_yadisk}",
        }

    async def get_url_for_upload(
        self, id: UUID, name: str, surname: str, file: UploadFile
    ) -> str | bool:
        method = "resources/upload"
        path_for_upload = (
            f"{self.url}{method}?path=/mini_shop/{id}_{name}_{surname}_{file.filename}"
        )
        headers = self.get_headers_ya_disk()
        async with aiohttp.ClientSession(headers=headers) as session:
            async with session.get(url=path_for_upload) as resp:
                if resp.status == 200:
                    response = await resp.json()
                    url_for_upload = response["href"]
                    return url_for_upload
                else:
                    return False

    async def upload_photo(self, url: str, file: UploadFile) -> str | bool:
        headers = self.get_headers_ya_disk()
        async with aiohttp.ClientSession(headers=headers) as session:
            async with session.put(url=url, data=file.file) as resp:
                if resp.status == 201:
                    return file.filename
                else:
                    return False


yandex_client = YandexClient()
