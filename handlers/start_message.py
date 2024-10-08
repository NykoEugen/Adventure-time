import logging

from aiogram import types
from aiogram.dispatcher.router import Router
from aiogram.filters import Command

from utils.db import db, create_collection
from keyboards.inline_keyboards import inline_keyboard

router = Router()
logger = logging.getLogger("Main")

@router.message(Command('start'))
async def start_handler(message: types.Message):
    kb = inline_keyboard(new_game="New game", load_game="Load game")
    await message.answer("Витаю вас у грі: Час пригод")

    user_id = message.from_user.id
    item = {"user_id": user_id}
    await create_collection("users", "user_id")
    collection = db.users

    exist_user = await db.users.find_one({"user_id": user_id})

    if exist_user:
        await message.answer("Радий знову тебе бачити", reply_markup=kb)

    else:
        result = await collection.insert_one(item)
        logger.info(f"Document inserted with ID: {result.inserted_id}")
        await message.answer("Вас додано до гри", reply_markup=kb)
