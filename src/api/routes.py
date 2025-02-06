
from fastapi import APIRouter, Depends
from dependency_injector.wiring import inject, Provide

from ..containers import Container
from ..jobs.kafka_jods import KafkaJobHelper
from ..services import GameService

router = APIRouter()

@router.get("/")
async def root():
    return {"Kafka": "Spiderweb"}

@router.get("/start")
@inject
async def start_game(game_service: GameService = Depends(Provide[Container.game_service])):
    spidey_order = game_service.spidey_random(game_service.spidey_names)
    await game_service.kafka_service.send_message(spidey_order)
    return {"order": spidey_order}

@router.get("/messages")
@inject
async def get_kafka_messages():
    job = KafkaJobHelper()
    messages = await job.load_spiderweb_messages()
    return messages


@router.get("/nevada/messages")
@inject
async def get_nevada_messages():
    job = KafkaJobHelper()
    messages = await job.load_nevada_messages()
    return messages
