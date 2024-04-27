from fastapi import APIRouter, Depends
from punq import Container

from application.contracts.neural_networks.create_neural_network_request import (
    CreateNeuralNetworkRequest,
)
from application.usecases.neural_network import NeuralNetworkService
from domain.neural_networks.model import Model
from infrastructure.di.container import get_container

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


@model_router.get("/{model_name}", response_model=Model)
async def get_model(
    model_name: str,
    container: Container = Depends(get_container),
):
    neural_network_service: NeuralNetworkService = container.resolve(
        NeuralNetworkService
    )
    return await neural_network_service.get_by_name(model_name)
