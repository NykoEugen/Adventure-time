import logging
from gc import collect

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


async def create_collection(collection_name, index_name):
    if collection_name not in await db.list_collection_names():
        try:
            await db.create_collection(collection_name)
            logger.info(f"Collection '{collection_name}' created.")

            collection = db[collection_name]
            existing_indexes = await collection.index_information()

            if index_name:
                if index_name not in existing_indexes:
                    await collection.create_index(index_name, unique=True)
                    logger.info(f"Created unique index for '{index_name}.")
                else:
                    logger.info(f"Index for {index_name} already exists.")

        except Exception as e:
            logger.error(f"Failed to create collection '{collection_name}': {e}")


async def save_to_db(collection, character_id, all_param):
    data = db[collection]
    character = await data.find_one(({"character_id": character_id}))
    if character:
        result = await data.update_one({"character_id": character_id}, {"$set": all_param})
        if result.modified_count > 0:
            logger.info(f"Character update successful")
    else:
        result = await data.insert_one(all_param)
        if result.inserted_id:
            logger.info(f"Character add successful {result.inserted_id}")


async def load_from_db(collection, character_id):
    data = db[collection]
    character = await data.find_one(({"character_id": character_id}))
    if character:
        logger.info("Character founds")
        return character
    else:
        logger.info("Not found")
        return None


async def close_connection():
    client.close()
