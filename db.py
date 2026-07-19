import os
from services.config import Config
from pymongo import MongoClient

mongo_uri = Config.MONGO_URI
db_name = Config.MONGO_DATABASE

client = MongoClient(mongo_uri)
db = client[db_name]