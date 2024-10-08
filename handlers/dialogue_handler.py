import logging
from random import randint

from aiogram import Router
from aiogram.types import CallbackQuery

from keyboards.inline_keyboards import inline_keyboard_actions
from utils.ai_generation import get_chatgpt_response
from utils.determinate_action_type import possible_action_str, determine_action_types
from utils.load_json import load_json
from utils.parse_text_and_actions import parse_text_and_actions

router = Router()
logger = logging.getLogger("Main")


@router.callback_query(lambda callback: callback.data.startswith("dialogue:"))
async def handle_action_callback(callback: CallbackQuery):
    action = callback.data.split(":", 1)[1]
    character_id = callback.from_user.id
    await callback.answer()

    game_context = load_json("text-templates/game-context.json")
    if game_context["character_id"] == character_id:
        game_context["actions"].append(action)
        game_context["last_action"] = action.lower()
        num_actions = randint(1, 5)

        prompt = (
            f"{game_context['conversation'][-1]} You decided to {action.lower()} whats happend next. Generate a dialogue with NPC"
            f"base on context, {num_actions} dialogue acts"
            f"Format for dialogue text 4 sentences, and at the end, list up to {num_actions} possible actions {possible_action_str} "
            f"that the player can take, always separate them by Possible actions:, 2-3 words for possible actions")

        request = await get_chatgpt_response(prompt)
        logger.info(request)
        dialogue_data, actions = parse_text_and_actions(request)
        actions_type = determine_action_types(actions)

        game_context["conversation"].append(dialogue_data)
        kb = inline_keyboard_actions(actions_type)

        await callback.message.answer(f"{dialogue_data}", reply_markup=kb)
