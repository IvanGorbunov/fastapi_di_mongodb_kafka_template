import asyncio

from src.app import create_app

app = create_app()


async def consume_messages():
    kafka_service = app.container.kafka_service_spiderweb()
    game_service = app.container.game_service()
    await kafka_service.consume_messages(game_service.process_turn)


@app.on_event("startup")
async def startup_event():
    asyncio.create_task(consume_messages())


if __name__ == "__main__":
    import uvicorn

    # logger.getlogger().info("The app started.")
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
