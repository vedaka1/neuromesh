import os
import re
from uuid import uuid4

import aiohttp


class TwitterGateway:
    block_size = 1024
    api_url = 'https://twitsave.com/info?url='
    download_link_pattern = r'href="(https://twitsave.com/download[^"]+)"'

    async def _download_to_file(self, url: str, session: aiohttp.ClientSession) -> None:
        download_path = self.get_download_path()
        response = await session.get(url)
        file_name = f'{download_path}/{str(uuid4())}.mp4'

        with open(file_name, 'wb') as file:
            while True:
                chunk = await response.content.read(self.block_size)
                if not chunk:
                    break
                file.write(chunk)

    async def _download_to_buffer(self, url: str, session: aiohttp.ClientSession) -> bytes:
        response = await session.get(url)
        buffer = await response.content.read()
        return buffer

    def get_download_path(self) -> str:
        download_path = f'{os.path.abspath(os.getcwd())}/tmp'
        os.makedirs(download_path, exist_ok=True)
        return download_path

    async def download_video(self, url: str) -> bytes | None:
        session = aiohttp.ClientSession()
        response = await session.get(self.api_url + url)
        html_string = await response.text()

        match_href = re.search(self.download_link_pattern, html_string)
        try:
            if match_href:
                link = match_href.group(1)
                return await self._download_to_buffer(url=link, session=session)
            else:
                print('Link not found')
        finally:
            await session.close()
