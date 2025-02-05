from fastapi import APIRouter, Depends
from dependency_injector.wiring import inject, Provide
from ..services import GameService

router = APIRouter()

@router.get("/")
async def root():
    return {"Kafka": "Spiderweb"}

@router.get("/start")
@inject
async def start_game(game_service: GameService = Depends(Provide["Container.game_service"])):
    spidey_order = game_service.spidey_random(game_service.spidey_names)
    await game_service.kafka_service.send_message(spidey_order)
    return {"order": spidey_order}

@router.get("/messages")
@inject
async def get_kafka_messages(
    limit: int = 10,
    kafka_service: KafkaService = Depends(Provide["Container.kafka_service"])
):
    """ Получает последние `limit` сообщений из Kafka """
    messages = []
    async def callback(msg):
        messages.append(msg)
        if len(messages) >= limit:
            return messages

    await kafka_service.consume_messages(callback)
    return {"messages": messages}
