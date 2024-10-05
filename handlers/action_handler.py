import json
import logging

from aiogram import Router
from aiogram.types import CallbackQuery

from handlers.ai_generation import get_chatgpt_response
from keyboards.inline_keyboards import inline_keyboard_actions
from utils.parse_text_and_actions import parse_text_and_actions
from utils.load_json import load_json, save_json

router = Router()
logger = logging.getLogger("Main")


@router.callback_query(lambda callback: callback.data.startswith("action:"))
async def handle_action_callback(callback: CallbackQuery):
    action = callback.data.split(":", 1)[1]

    game_context = load_json("text-templates/game-context.json")
    game_context["actions"].append(action)
    game_context["last_action"] = action.lower()

    prompt = (f"{game_context['conversation'][-1]} You decided to {action.lower()}. 4 sentences, Please generate a narrative "
              f"with a description and dialogue, and at the end, list up to 5 possible actions that the player can take, "
              f"always separate them by **Possible actions:**, 2-3 words")

    result = await get_chatgpt_response(prompt)

    main_text, actions = parse_text_and_actions(result)

    kb = inline_keyboard_actions(actions)

    game_context["conversation"].append(main_text)
    save_json(game_context)

    await callback.message.answer(result, reply_markup=kb)
    await callback.answer()
