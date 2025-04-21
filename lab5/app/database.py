import motor.motor_asyncio

MONGO_URL = "mongodb://mongo_admin:password@mongo_db:27017"
client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URL)
db = client.books
books_collection = db.get_collection("books")
