from typing import Annotated

from dishka.integrations.fastapi import DishkaRoute, FromDishka
from fastapi import APIRouter, Depends

from application.contracts.neural_networks.create_neural_network_request import (
    CreateNeuralNetworkRequest,
)
from application.contracts.neural_networks.generate_response_request import (
    GenerateResponseRequest,
)
from application.usecases.neural_networks import *
from application.usecases.users.update_user import CheckUserSubscription
from domain.common.response import ModelResponse
from domain.neural_networks.model import Model
from infrastructure.tasks.tasks import generate_image_task

model_router = APIRouter(
    tags=["Neural Networks"],
    prefix="/models",
    route_class=DishkaRoute,
)


@model_router.post("", response_model=Model, summary="Create a neural network")
async def create_model(
    create_model_request: Annotated[CreateNeuralNetworkRequest, Depends()],
    create_neural_network_interactor: FromDishka[CreateNeuralNetwork],
) -> Model:
    return await create_neural_network_interactor(create_model_request)


@model_router.get(
    "",
    response_model=list[Model],
    summary="Get a list of available neural networks",
)
async def get_all_models(
    get_all_neural_networks_interactor: FromDishka[GetAllNeuralNetworks],
) -> list[Model]:
    return await get_all_neural_networks_interactor()


@model_router.get(
    "/{model_name}",
    response_model=Model,
    summary="Get information about the neural network",
)
async def get_model(
    model_name: str,
    get_neural_network_by_name_interactor: FromDishka[GetNeuralNetworkByName],
) -> Model:
    return await get_neural_network_by_name_interactor(model_name)


@model_router.post(
    "/response",
    response_model=ModelResponse,
    summary="Send a request to generate a text response",
)
async def generate_response(
    generate_response_request: GenerateResponseRequest,
    generate_response_interactor: FromDishka[GenerateResponse],
    check_user_subscription_interactor: FromDishka[CheckUserSubscription],
) -> ModelResponse:
    await check_user_subscription_interactor(generate_response_request.user_id)
    return await generate_response_interactor(generate_response_request)


@model_router.post("/image", summary="Send a request to generate an image")
async def generate_image(
    user_id: int,
    user_prompt: str,
) -> None:
    await generate_image_task.kiq(user_id=user_id, user_prompt=user_prompt)
    return None


@model_router.delete(
    "/{model_name}",
    summary="Delete a neural network by name",
)
async def delete_model(
    model_name: str,
    delete_neural_network_interactor: FromDishka[DeleteNeuralNetwork],
) -> None:
    await delete_neural_network_interactor(model_name)
    return None
