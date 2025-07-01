import logging
from dataclasses import dataclass

from dotenv import load_dotenv

from .base import getenv

def init_logging():
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    handler = logging.FileHandler("app.log")


@dataclass
class Port:
    port: str

@dataclass
class Host:
    host: str


@dataclass
class GptApi:
    gpt_key: str
    model: str


@dataclass
class Db:
    db_url: str
    db_name: str


@dataclass
class Config:
    port: Port
    host: Host
    db: Db
    gpt_key: GptApi
    


def load_config() -> Config:
    load_dotenv()
    return Config(
        port=Port(port=getenv("PORT")),
        host=Host(host=getenv("HOST")),
        db=Db(db_url=getenv("DB_URL"),
                  db_name=getenv('DB_NAME')),
        gpt_key=GptApi(gpt_key=getenv("GEMINI_KEY"), model=getenv('GEMINI_MODEL'))
    )
