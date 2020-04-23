import logging

import uvicorn
from fastapi import FastAPI

from src.api.api import api_router
from src.core.config import LOGGING_CONFIG, configure_inject
from src.core.db import db

LOGGER = logging.getLogger(__name__)


def create_app():
    try:
        LOGGER.info("Initiliase fast-API app")
        app = FastAPI()
        db.init_app(app=app)
        configure_inject()
        app.include_router(api_router)
    except Exception as e:
        LOGGER.error(f"Error in fast-API app initialisation => {e}")
    return app


app = create_app()


@app.on_event("startup")
async def _startup() -> None:
    try:
        LOGGER.info("Create tables")
        # await db.gino.drop_all()
        await db.gino.create_all()
    except Exception as e:
        LOGGER.error(f"Error in startup for tables creation => {e}")


def run():
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="debug",
        access_log=True,
        log_config=LOGGING_CONFIG,
    )