import os
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase


MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
DB_NAME = os.getenv("DB_NAME", "todo_db")

client = AsyncIOMotorClient(MONGO_URI)
_db: AsyncIOMotorDatabase = client[DB_NAME]

async def get_db() -> AsyncIOMotorDatabase:
    # Intentar crear la colección si no existe
    try:
        await _db.create_collection("tasks", capped=False)
    except Exception:
        # Si ya existe, ignorar el error
        pass
    return _db