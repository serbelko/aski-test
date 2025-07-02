from fastapi import FastAPI
import uvicorn
import logging

from config import config, init_logging
from config import init_mongo
from src.api import router

app = FastAPI()
init_logging()
logger = logging.getLogger(__name__)

app = FastAPI()
app.include_router(router)

if __name__ == "__main__":
    init_mongo()
    logger.info("Приложение запущенно") 
    uvicorn.run(
        app,
        host=config.host.host,
        port=int(config.port.port))