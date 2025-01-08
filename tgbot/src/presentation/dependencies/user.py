from typing import Any

from httpx import AsyncClient


async def get_user(tg_id: int, client: AsyncClient) -> dict[str, Any]:
    repsponse = await client.get(f'/users/{tg_id}')
    user = repsponse.json()
    repsponse.raise_for_status()
    return user
