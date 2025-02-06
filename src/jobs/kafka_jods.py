import asyncio
from abc import ABC
from typing import List, Dict

from dependency_injector.wiring import Provide
from fastapi import Depends

from src.containers import Container
from src.services import KafkaService, kafka_service


class AbstractKafkaJobHelper(ABC):

    async def _get_meggases(self, service: KafkaService) -> Dict[str, List[str]]:
        ...


class BaseKafkaJobHelper(AbstractKafkaJobHelper):
    def __init__(self, limit: int = 10, timeout: int = 5):
        self._limit = limit
        self._timeout = timeout
    async def _get_meggases(self, service: KafkaService) -> Dict[str, List[str]]:
        messages = []
        event = asyncio.Event()

        async def callback(msg):
            messages.append(msg)
            if len(messages) >= self._limit:
                event.set()

        consumer_task = asyncio.create_task(service.consume_messages(callback))

        try:
            await asyncio.wait_for(event.wait(), timeout=self._timeout)
        except asyncio.TimeoutError:
            consumer_task.cancel()

        return {"messages": messages}

class KafkaJobHelper(BaseKafkaJobHelper):


    async def load_spiderweb_messages(
            self,
            kafka_service: KafkaService = Depends(Provide[Container.kafka_service_spiderweb])
    ) -> Dict[str, List[str]]:
        return await self._get_meggases(service=kafka_service)

    async def load_nevada_messages(
            self,
            kafka_service: KafkaService = Depends(Provide[Container.kafka_service_nevada]),
    ) -> Dict[str, List[str]]:
        return await self._get_meggases(service=kafka_service)