from pymongo import MongoClient
from app.config import get_settings

settings = get_settings()

class CopusMongoDB:
    client: MongoClient = None

    @classmethod
    def connect_to_mongodb(cls):
        cls.client = MongoClient(settings.mongodb_connection_string)
        
    @classmethod
    def close_mongodb_connection(cls):
        if cls.client:
            cls.client.close()

    @classmethod
    def get_documents(cls):
        db = cls.client[settings.mongodb_db_name]
        collection = db[settings.mongodb_collection_name]
        documents = []
        for document in collection.find({}):
            documents.append({
                'content': document['content'],
                'uuid': document['uuid']
            })
        return documents

    @classmethod
    def get_document(cls, uuid: str):
        db = cls.client[settings.mongodb_db_name]
        collection = db[settings.mongodb_collection_name]
        return collection.find_one({"uuid": uuid}) 