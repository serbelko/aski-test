from fastapi import FastAPI
from config.session import init_mongo
import uvicorn


app = FastAPI()

from config import load_config
from src.api import router

app = FastAPI()
app.include_router(router)

if __name__ == "__main__":
    init_mongo()

    config = load_config()
    uvicorn.run(
        app,
        host=config.host.host,
        port=int(config.port.port))