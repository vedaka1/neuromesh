from httpx import AsyncClient


class AsyncTGClient(AsyncClient):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
