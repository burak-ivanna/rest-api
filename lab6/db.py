from pymongo import MongoClient

client = MongoClient(
    "mongodb://mongo_admin:password@mongo:27017/",
    authSource="admin"
)
db = client["books"]
collection = db["library"]
