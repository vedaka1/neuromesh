# @pytest.fixture(scope="function")
# async def subscription_repository(container: AsyncContainer):
#     async with container() as di_container:
#         subscription_repository = di_container.get(BaseSubscriptionRepository)
#         yield subscription_repository
