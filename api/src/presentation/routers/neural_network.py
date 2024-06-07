from dishka.integrations.fastapi import DishkaRoute, FromDishka
from fastapi import APIRouter, Depends
from punq import Container

from application.contracts.neural_networks.create_neural_network_request import (
    CreateNeuralNetworkRequest,
)
from application.contracts.neural_networks.generate_response_request import (
    GenerateResponseRequest,
)
from application.usecases.neural_networks import *
from domain.common.response import ModelResponse
from domain.neural_networks.model import Model
from infrastructure.di.container_old import get_container

model_router = APIRouter(
    tags=["Neural Networks"],
    prefix="/models",
    route_class=DishkaRoute,
)


@model_router.post("", response_model=Model)
async def create_model(
    create_model_request: CreateNeuralNetworkRequest,
    container: Container = Depends(get_container),
):
    create_neural_network_interactor: CreateNeuralNetwork = container.resolve(
        CreateNeuralNetwork
    )
    return await create_neural_network_interactor(create_model_request)


@model_router.get("", response_model=list[Model])
async def get_all_models(
    get_all_neural_networks_interactor: FromDishka[GetAllNeuralNetworks],
):
    return await get_all_neural_networks_interactor()


@model_router.get("/{model_name}", response_model=Model)
async def get_model(
    model_name: str,
    get_neural_network_by_name_interactor: FromDishka[GetNeuralNetworkByName],
):
    return await get_neural_network_by_name_interactor(model_name)


@model_router.post("/response", response_model=ModelResponse)
async def generate_response(
    generate_response_request: GenerateResponseRequest,
    generate_response_interactor: FromDishka[GenerateResponse],
):
    return await generate_response_interactor(generate_response_request)
