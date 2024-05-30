from httpx import AsyncClient


async def get_user(tg_id: int, client: AsyncClient) -> dict | None:
    try:
        data = await client.get(f"/users/{tg_id}")
        user = data.json()
    except:
        return None
    return user
