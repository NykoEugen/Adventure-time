import logging

from aiogram import Router, types
from aiogram.filters import Command

from handlers.ai_generation import get_chatgpt_response

router = Router()
logger = logging.getLogger("Main")

@router.message(Command('promt'))
async def promt_handler(message: types.Message):

    result = await get_chatgpt_response("Створити опис середньовікової ковальні в стіли фентезі, 3 речень")
    logger.info(result)
    await message.answer(result)

