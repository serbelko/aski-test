from pymongo import MongoClient
from config.config import load_config

mongo_client: MongoClient = None
aski_db = None

def init_mongo():
    global mongo_client, aski_db
    config = load_config()
    mongo_client = MongoClient(config.db.db_url, serverSelectionTimeoutMS=5000)
    aski_db = mongo_client[config.db.db_name]

def get_collection(name: str):
    if aski_db is None:
        raise RuntimeError("MongoDB is not initialized. Call init_mongo() first.")
    return aski_db[name]
