import logging
from random import randint

from aiogram import Router
from aiogram.types import CallbackQuery

from keyboards.inline_keyboards import inline_keyboard_actions
from quests.base_quest import QuestHandler
from utils.ai_generation import get_chatgpt_response
from utils.db import create_collection
from utils.determinate_action_type import possible_action_str, determine_action_types
from utils.load_json import load_json
from utils.parse_text_and_actions import parse_quest_text

router = Router()
logger = logging.getLogger("Main")


@router.callback_query(lambda callback: callback.data.startswith("quest:"))
async def handle_action_callback(callback: CallbackQuery):
    action = callback.data.split(":", 1)[1]
    character_id = callback.from_user.id
    await callback.answer()

    num_actions = randint(1, 5)
    game_context = load_json("text-templates/game-context.json")
    location = game_context["location"]
    prompt = (f"{game_context['conversation'][-1]} You decided to {action.lower()} whats happend next. Generate a quest with goal and reward"
              f"and description base on context."
              "Format for quest: '{"
              "'quest_goal': 'goal',"
              "'quest_reward': 'reward',"
              "'quest_description': 'description'"
              "}'"
              f" 3 sentences, and at the end, list up to {num_actions} possible actions {possible_action_str} that the player can take, "
              f"always separate them by Possible actions:, 2-3 words for possible actions")
    request = await get_chatgpt_response(prompt)
    quest_data, actions = parse_quest_text(request)

    quest = QuestHandler(quest_data, location)
    # quest.start_quest(character_id)
    if character_id not in quest.state:
        quest.start_quest(character_id)

        # Оновлюємо стан квесту на основі дії гравця
    quest.update_quest_state(character_id, action)

    action_type = determine_action_types(actions)

    await create_collection("quests", "character_id")

    kb = inline_keyboard_actions(action_type)

    quest_goal = quest_data['quest_goal']
    quest_reward = quest_data['quest_reward']

    await callback.message.answer(f"Choose a quest {quest_goal}, {quest_reward}", reply_markup=kb)
