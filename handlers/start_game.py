import asyncio
import logging

from aiogram import Router
from aiogram.types import CallbackQuery

from handlers.ai_generation import get_chatgpt_response
from handlers.db import load_character
from keyboards.inline_keyboards import inline_keyboard_actions
from utils.load_json import load_json, save_json, initialize_json

router = Router()
logger = logging.getLogger("Main")


@router.callback_query(lambda callback: callback.data == "start_game")
async def handle_start_game(callback: CallbackQuery):
    character_id = callback.from_user.id

    initialize_json("text-templates/game-context.json", {
        "character_id": None,
        "character_type": None,
        "character_name": None,
        "location": [],
        "conversation": [],
        "actions": [],
        "last_action": ""
    })

    start_location = "Medieval fantasy town"
    game_context = load_json("text-templates/game-context.json")
    game_context["location"].append(start_location)
    game_context["character_id"] = character_id

    text = load_json("text-templates/game-promts.json")
    logger.info("Text from json added")
    character = await load_character(character_id)
    intro = text["intro"]["description"].format(location=start_location, character_name=character["character_name"], character_type=character["character_type"])

    game_context["character_type"] = character["character_type"]
    game_context["character_name"] = character["character_name"]

    await callback.message.answer("YOU JOURNEY STARTS NOW!")
    response = await get_chatgpt_response(intro)

    game_context["conversation"].append(response)
    save_json(game_context)

    actions = text["intro"]["actions"]
    kb = inline_keyboard_actions(actions)
    await asyncio.sleep(2)
    await callback.message.answer(response, reply_markup=kb)
    await callback.answer()
