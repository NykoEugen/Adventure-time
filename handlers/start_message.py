import logging

from aiogram import types
from aiogram.dispatcher.router import Router
from aiogram.filters import Command

from handlers.db import db, create_collection

router = Router()
logger = logging.getLogger("Main")

@router.message(Command('start'))
async def start_handler(message: types.Message):
    await message.answer("Привіт! Я підключений і готовий до роботи 🎉")

    user_id = message.from_user.id
    item = {"user_id": user_id}
    await create_collection("users")
    collection = db.users

    exist_user = await db.users.find_one({"user_id": user_id})

    if exist_user:
        result = await db.users.update_one({"user_id": user_id}, {"$set": {"sex": "female"}})
        if result.modified_count > 0:
            await message.answer("New field added successfully!")
        else:
            await message.answer("No changes were made to the document.")


    result = await collection.insert_one(item)
    logger.info(f"Document inserted with ID: {result.inserted_id}")
