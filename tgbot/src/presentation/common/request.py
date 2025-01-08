# def request(func):
#     @functools.wraps(func)
#     async def wrapper(*args, **kwargs):
#         try:
#             print("ff")
#             return await func(*args, **kwargs)
#         except HTTPStatusError as e:
#             print(e)
#             await message.answer(Response(f"Error: {e.response.json()["detail"]}").value)
#         except Exception as e:
#             print(e)
#             await message.answer(f"Неизвестная ошибка")
#     return wrapper
