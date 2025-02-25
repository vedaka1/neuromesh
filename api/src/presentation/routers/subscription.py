from application.contracts.subscriptions.create_subscription_request import (
    CreateSubscriptionRequest,
)
from application.contracts.subscriptions.get_subscription_response import (
    GetSubscriptionResponse,
)
from application.usecases.subscriptions.create_subscription import CreateSubscription
from application.usecases.subscriptions.delete_subscription import DeleteSubscription
from application.usecases.subscriptions.get_subscription import GetAllSubscriptions, GetSubscriptionByName
from application.usecases.subscriptions.update_subscription import (
    AddModelToSubscription,
    DeleteModelFromSubscription,
)
from dishka.integrations.fastapi import DishkaRoute, FromDishka
from domain.neural_networks.model import ModelSubscription
from domain.subscriptions.subscription import Subscription
from fastapi import APIRouter

subscription_router = APIRouter(
    tags=['Subscriptions'],
    prefix='/subscriptions',
    route_class=DishkaRoute,
)


@subscription_router.post('', response_model=Subscription, summary='Create a subscription')
async def create_subscription(
    create_subscription_request: CreateSubscriptionRequest,
    create_subscription_interactor: FromDishka[CreateSubscription],
) -> Subscription:
    return await create_subscription_interactor(create_subscription_request)


@subscription_router.get('', response_model=list[Subscription], summary='Get a list of available subscriptions')
async def get_subscriptions(
    get_all_subscriptions_interactor: FromDishka[GetAllSubscriptions],
) -> list[Subscription]:
    return await get_all_subscriptions_interactor()


@subscription_router.get(
    '/{subscription_name}', response_model=GetSubscriptionResponse, summary='Get a subscription by name'
)
async def get_subscription(
    subscription_name: str,
    get_subscription_by_name_interactor: FromDishka[GetSubscriptionByName],
) -> GetSubscriptionResponse:
    return await get_subscription_by_name_interactor(subscription_name)


@subscription_router.post(
    '/{subscription_name}', response_model=ModelSubscription, summary='Add a neural model to the subscription'
)
async def add_model_to_subscription(
    subscription_name: str,
    model_name: str,
    default_requests: int,
    add_model_to_subscription_interactor: FromDishka[AddModelToSubscription],
) -> ModelSubscription:
    return await add_model_to_subscription_interactor(
        subscription_name=subscription_name,
        model_name=model_name,
        requests=default_requests,
    )


@subscription_router.delete('/{subscription_name}', summary='Delete a subscription by name')
async def delete_subscription(
    subscription_name: str,
    delete_subscription_interactor: FromDishka[DeleteSubscription],
) -> None:
    return await delete_subscription_interactor(subscription_name)


@subscription_router.delete('/{subscription_name}/{model_name}', summary='Delete a neural network from subscription')
async def delete_model_from_subscription(
    subscription_name: str,
    model_name: str,
    delete_model_from_subscription_interactor: FromDishka[DeleteModelFromSubscription],
) -> None:
    return await delete_model_from_subscription_interactor(subscription_name, model_name)
