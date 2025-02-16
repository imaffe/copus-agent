from motor.motor_asyncio import AsyncIOMotorClient
from app.config import get_settings

settings = get_settings()

class CopusMongoDB:
    client: AsyncIOMotorClient = None

    @classmethod
    async def connect_to_mongodb(cls):
        cls.client = AsyncIOMotorClient(settings.mongodb_connection_string)
        
    @classmethod
    async def close_mongodb_connection(cls):
        if cls.client:
            cls.client.close()

    @classmethod
    async def get_documents(cls):
        db = cls.client[settings.mongodb_db_name]
        collection = db[settings.mongodb_collection_name]
        cursor = collection.find({})
        documents = []
        async for document in cursor:
            documents.append({
                'content': document['content'],
                'uuid': document['uuid']
            })
        return documents

    @classmethod
    async def get_document(cls, uuid: str):
        db = cls.client[settings.mongodb_db_name]
        collection = db[settings.mongodb_collection_name]
        return await collection.find_one({"uuid": uuid}) 