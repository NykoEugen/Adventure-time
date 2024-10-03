import logging

from aiogram import Router
from aiogram.types import CallbackQuery

from handlers.db import load_character
from keyboards.inline_keyboards import inline_keyboard

router = Router()
logger = logging.getLogger("Main")


@router.callback_query(lambda callback: callback.data == "load_game")
async def handle_character_type(callback: CallbackQuery):
    user_id = callback.from_user.id
    character = await load_character(user_id)
    if character:
        character_name = character['character_name']
        character_type = character['character_type']
        kb_title = f"{character_type} {character_name}"
        kb = inline_keyboard(load_character=kb_title)
        await callback.message.answer("You have character", reply_markup=kb)
        await callback.answer()

    else:
        kb = inline_keyboard(new_game="Create Character")
        await callback.message.answer("You don't have character yet", reply_markup=kb)
        await callback.answer()