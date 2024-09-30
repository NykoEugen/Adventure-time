import logging

from motor.motor_asyncio import AsyncIOMotorClient

from config import DB_URL

logger = logging.getLogger("Main")

client = AsyncIOMotorClient(DB_URL)
db = client.mongodb

async def check_connection():
    try:
        await client.admin.command('ping')
        logger.info("Successfully connected to MongoDB")
    except Exception as e:
        logger.error(f"Failed to connect to MongoDB: {e}")
        raise e

async def create_collection(collection_name):
    if collection_name not in await db.list_collection_names():
        try:
            await db.create_collection(collection_name)
            logger.info(f"Collection '{collection_name}' created.")
        except Exception as e:
            logger.error(f"Failed to create collection '{collection_name}': {e}")

async def save_hero_changes(character_id, all_param):
    collection = db.characters
    character = await collection.find_one(({"character_id": character_id}))
    if character:
        result = await collection.update_one({"character_id": character_id}, {"$set": {all_param}})
        if result.modified_count > 0:
            logger.info(f"Character changes save successful {result.inserted_id}")
    else:
        result = await collection.insert_one(all_param)
        if result.inserted_id:
            logger.info(f"Character changes save successful {result.inserted_id}")

async def close_connection():
    client.close()
