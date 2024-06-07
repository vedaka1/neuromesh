from fastapi import APIRouter, Depends
from punq import Container

from application.contracts.subscriptions.create_subscription_request import (
    CreateSubscriptionRequest,
)
from application.contracts.subscriptions.get_subscription_response import (
    GetSubscriptionResponse,
)
from application.usecases.subscriptions import *
from domain.neural_networks.model import ModelSubscription
from domain.subscriptions.subscription import Subscription
from infrastructure.di.container import get_container

subscription_router = APIRouter(
    tags=["Subscriptions"],
    prefix="/subscriptions",
)


@subscription_router.post("", response_model=Subscription)
async def create_subscription(
    create_subscription_request: CreateSubscriptionRequest,
    container: Container = Depends(get_container),
):
    create_subscription_interactor: CreateSubscription = container.resolve(
        CreateSubscription
    )
    return await create_subscription_interactor(create_subscription_request)


@subscription_router.get("", response_model=list[Subscription])
async def get_subscriptions(
    container: Container = Depends(get_container),
):
    get_all_subscriptions_interactor: GetAllSubscriptions = container.resolve(
        GetAllSubscriptions
    )
    return await get_all_subscriptions_interactor()


@subscription_router.get("/{subscription_name}", response_model=GetSubscriptionResponse)
async def get_subscription(
    subscription_name: str,
    container: Container = Depends(get_container),
):
    get_subscription_by_name_interactor: GetSubscriptionByName = container.resolve(
        GetSubscriptionByName
    )
    return await get_subscription_by_name_interactor(subscription_name)


@subscription_router.post("/{subscription_name}", response_model=ModelSubscription)
async def add_model_to_subscription(
    subscription_name: str,
    model_name: str,
    default_requests: int,
    container: Container = Depends(get_container),
):
    add_model_to_subscription_interactor: AddModelToSubscription = container.resolve(
        AddModelToSubscription
    )
    return await add_model_to_subscription_interactor(
        subscription_name=subscription_name,
        model_name=model_name,
        requests=default_requests,
    )
