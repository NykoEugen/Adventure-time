import logging

from aiogram import Router
from aiogram.types import CallbackQuery

router = Router()
logger = logging.getLogger("Main")


@router.callback_query(lambda callback: callback.data.startswith("battle:"))
async def handle_action_callback(callback: CallbackQuery):
    action = callback.data.split(":", 1)[1]
    await callback.answer()

    await callback.message.answer(f"Choose a battle {action}")