import logging

from aiogram import Router, types
from aiogram.filters import Command

from character.base_classes import Warrior
from handlers.db import db, create_collection, save_hero_changes

router = Router()
logger = logging.getLogger("Main")

@router.message(Command('createhero'))
async def start_handler(message: types.Message):
    await message.answer("Створюємо персонажа")

    user_id = message.from_user.id
    await create_collection("characters")

    character = Warrior(user_id, "Conan")
    await character.save_character_state()

    await message.answer("New character create successfully!")
