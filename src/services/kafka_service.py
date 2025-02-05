import asyncio
import json
from aiokafka import AIOKafkaProducer, AIOKafkaConsumer
from typing import List

class KafkaService:
    def __init__(self, bootstrap_servers: str, topic: str):
        self.bootstrap_servers = bootstrap_servers
        self.topic = topic
        self.loop = asyncio.get_event_loop()

    def kafka_serializer(self, value):
        return json.dumps(value).encode("utf-8")

    async def send_message(self, msg: List):
        producer = AIOKafkaProducer(
            bootstrap_servers=self.bootstrap_servers,
            value_serializer=self.kafka_serializer
        )
        await producer.start()
        try:
            await producer.send_and_wait(self.topic, msg)
        finally:
            await producer.stop()

    async def consume_messages(self, callback):
        consumer = AIOKafkaConsumer(
            self.topic,
            bootstrap_servers=self.bootstrap_servers,
            value_deserializer=lambda x: json.loads(x.decode("utf-8")),
            auto_offset_reset="latest",
            enable_auto_commit=True
        )

        await consumer.start()
        try:
            async for msg in consumer:
                await callback(msg.value)
        finally:
            await consumer.stop()
