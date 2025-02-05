import asyncio
import json
import logging
import os
from typing import List
from random import shuffle

from aiokafka import AIOKafkaConsumer, AIOKafkaProducer
from dotenv import load_dotenv
from fastapi import FastAPI

logger = logging.getLogger(__name__)

app = FastAPI()
load_dotenv()
loop = asyncio.get_event_loop()

spidey_names: List[str] = os.environ.get("SPIDEY_NAMES", "").split(",")
kafka_bootstrap_servers: str = os.environ.get("KAFKA_BOOTSTRAP_SERVERS", "")
spiderweb_topic: str = os.environ.get("SPIDERWEB_TOPIC", "")
my_name: str = os.environ.get("MY_NAME", "")

mapping_place = {
    3: "name is the Winner!!!",
    2: "name is the Second Place!!!",
    1: "name is the Third Place!!!",
}


def spidey_random(spidey_list: List) -> List:
    shuffle(spidey_list)
    return spidey_list


async def play_turn(finalists: List):
    spidey_order = spidey_random(finalists)
    await send_one(topic=spiderweb_topic, msg=spidey_order)


def kafka_serializer(value):
    return json.dumps(value).encode("utf-8")


def check_spidey(finalists: List) -> bool:
    return my_name == finalists[0]


async def send_one(topic: str, msg: List):
    """ Corrected send_one function """
    try:
        producer = AIOKafkaProducer(
            bootstrap_servers=kafka_bootstrap_servers,
            value_serializer=kafka_serializer,  # Corrected serialization
        )
        await producer.start()

        try:
            await producer.send_and_wait(topic, msg)
        finally:
            await producer.stop()

    except Exception as err:
        print(f"Kafka Error: {err}")


async def spiderweb_turn(msg):
    finalists = msg.value
    is_my_turn = check_spidey(finalists)

    if is_my_turn:
        print(mapping_place[len(finalists)].replace('name', my_name))

        if len(finalists) > 1:
            finalists.pop(0)
            await play_turn(finalists)


kafka_actions = {
    "spiderweb": spiderweb_turn,
}


async def consume():
    consumer = AIOKafkaConsumer(
        spiderweb_topic,
        loop=loop,
        bootstrap_servers=kafka_bootstrap_servers,
        value_deserializer=lambda x: json.loads(x.decode("utf-8")) if x else None,  # Corrected deserialization
    )

    try:
        await consumer.start()

    except Exception as e:
        print(f"Kafka Consumer Error: {e}")
        return

    try:
        async for msg in consumer:
            await kafka_actions[msg.topic](msg)

    finally:
        await consumer.stop()


asyncio.create_task(consume())


@app.get("/")
async def root():
    return {"Kafka": "Spiderweb"}


@app.get("/start")
async def start_game():
    spidey_order = spidey_random(spidey_names)
    await send_one(topic=spiderweb_topic, msg=spidey_order)

    return {"order": spidey_order}


@app.get("/messages")
async def get_kafka_messages(limit: int = 10):
    consumer = AIOKafkaConsumer(
        spiderweb_topic,
        bootstrap_servers=kafka_bootstrap_servers,
        value_deserializer=lambda x: json.loads(x.decode("utf-8")) if x else None,
        auto_offset_reset="latest",
        enable_auto_commit=True,
    )

    await consumer.start()

    messages = []

    try:
        await consumer.seek_to_end()
        async for msg in consumer:
            messages.append(msg.value)
            if len(messages) >= limit:
                break
    except Exception as e:
        print(f"Error consuming messages: {e}")
    finally:
        await consumer.stop()

    return {"messages": messages}
