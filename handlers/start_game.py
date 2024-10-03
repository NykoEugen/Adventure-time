import logging

from aiogram import Router
from aiogram.types import CallbackQuery

from handlers.ai_generation import get_chatgpt_response
from handlers.db import load_character
from utils.load_json import load_texts

router = Router()
logger = logging.getLogger("Main")


@router.callback_query(lambda callback: callback.data == "start_game")
async def handle_start_game(callback: CallbackQuery):
    character_id = callback.from_user.id
    text = load_texts("text-templates/game-promts.json")
    logger.info(text)
    character = await load_character(character_id)
    intro = text["intro"].format(character_name=character["character_name"], character_type=character["character_type"])

    response = await get_chatgpt_response(intro)
    await callback.message.answer(response)