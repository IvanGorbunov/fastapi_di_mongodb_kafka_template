from fastapi import FastAPI

from src.api.routes import router
from src.containers import Container


def create_app() -> FastAPI:
    # container = Container()
    # container.config.giphy.api_key.from_env("GIPHY_API_KEY")

    container = Container()
    container.config.from_dict({})

    app = FastAPI()
    app.container = container
    app.include_router(router)
    return app
