from application.contracts.neural_networks.create_neural_network_request import (
    CreateNeuralNetworkRequest,
)
from application.contracts.neural_networks.generate_response_request import (
    GenerateResponseRequest,
)
from application.usecases.neural_network import NeuralNetworkService
from domain.common.response import ModelResponse
from domain.neural_networks.model import Model
from fastapi import APIRouter, Depends
from infrastructure.di.container import get_container
from punq import Container

model_router = APIRouter(
    tags=["Neural Networks"],
    prefix="/models",
)


@model_router.post("", response_model=Model)
async def create_model(
    create_model_request: CreateNeuralNetworkRequest,
    container: Container = Depends(get_container),
):
    neural_network_service: NeuralNetworkService = container.resolve(
        NeuralNetworkService
    )
    return await neural_network_service.create(create_model_request)


@model_router.get("", response_model=list[Model])
async def get_all_models(
    container: Container = Depends(get_container),
):
    neural_network_service: NeuralNetworkService = container.resolve(
        NeuralNetworkService
    )
    return await neural_network_service.get_all()


@model_router.get("/{model_name}", response_model=Model)
async def get_model(
    model_name: str,
    container: Container = Depends(get_container),
):
    neural_network_service: NeuralNetworkService = container.resolve(
        NeuralNetworkService
    )
    return await neural_network_service.get_by_name(model_name)


@model_router.post("/response", response_model=ModelResponse)
async def generate_response(
    generate_response_request: GenerateResponseRequest,
    container: Container = Depends(get_container),
):
    neural_network_service: NeuralNetworkService = container.resolve(
        NeuralNetworkService
    )
    return await neural_network_service.generate_response(generate_response_request)
