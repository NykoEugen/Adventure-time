import json
import logging
from random import randint

from aiogram import Router
from aiogram.types import CallbackQuery

from handlers.ai_generation import get_chatgpt_response
from keyboards.inline_keyboards import inline_keyboard_actions
from utils.determinate_action_type import determine_action_types
from utils.parse_text_and_actions import parse_text_and_actions
from utils.load_json import load_json, save_json

router = Router()
logger = logging.getLogger("Main")


@router.callback_query(lambda callback: callback.data.startswith("generic:"))
async def handle_action_callback(callback: CallbackQuery):
    action = callback.data.split(":", 1)[1]
    await callback.answer()

    game_context = load_json("text-templates/game-context.json")
    game_context["actions"].append(action)
    game_context["last_action"] = action.lower()
    num_actions = randint(0, 5)

    prompt = (f"{game_context['conversation'][-1]} You decided to {action.lower()}. 4 sentences, Please generate a narrative "
              f"with a description and dialogue, and at the end, list up to {num_actions} possible actions that the player can take, "
              f"always separate them by **Possible actions:**, 2-3 words for possible actions")

    result = await get_chatgpt_response(prompt)

    main_text, actions = parse_text_and_actions(result)
    actions_type = determine_action_types(actions)
    kb = inline_keyboard_actions(actions_type)

    game_context["conversation"].append(main_text)
    save_json(game_context)

    await callback.message.answer(main_text, reply_markup=kb)

