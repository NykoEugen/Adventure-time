import asyncio
import logging

from aiogram import Router, types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, CallbackQuery

from character.base_classes import Warrior, Mage, Archer
from handlers.db import create_collection
from keyboards.inline_keyboards import inline_keyboard

router = Router()
logger = logging.getLogger("Main")


class CreateCharacterName(StatesGroup):
    waiting_for_name = State()


@router.callback_query(lambda callback: callback.data == "new_game")
async def handle_character_type(callback: CallbackQuery):
    kb = inline_keyboard(warrior="Warrior", mage="Mage", archer="Archer")
    await callback.answer()
    with open('text-templates/description_char_type.txt', 'r') as file:
        data = file.read()

    await callback.message.answer(data)
    await asyncio.sleep(2)
    await callback.message.answer("Choose character type:", reply_markup=kb)
    await callback.answer()

@router.callback_query(lambda callback: callback.data in {"warrior", "mage", "archer"})
async def choose_character_type(callback: CallbackQuery, state: FSMContext):
    character_id = callback.from_user.id
    character_type = callback.data
    await callback.answer()
    await state.update_data(character_type=character_type, character_id=character_id)
    await callback.message.answer(f"You choose {character_type}, create character name")
    await state.set_state(CreateCharacterName.waiting_for_name)
    await callback.answer()

@router.message(CreateCharacterName.waiting_for_name)
async def process_hero_name(message: types.Message, state: FSMContext):
    kb = inline_keyboard(save_character="Save character", new_game="Change character")
    character_name = message.text
    await state.update_data(character_name=character_name)
    data = await state.get_data()
    character_type = data.get("character_type")
    await message.answer(f"You character is a {character_type} and name is {character_name}, save changes?",
                         reply_markup=kb)

@router.callback_query(lambda callback: callback.data == "save_character")
async def save_new_character(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    data = await state.get_data()
    character_id = data.get("character_id")
    character_type = data.get("character_type")
    character_name = data.get("character_name")

    await create_collection("characters", "character_id")

    match character_type:
        case "warrior":
            character = Warrior(character_id, character_name)
        case "mage":
            character = Mage(character_id, character_name)
        case "archer":
            character = Archer(character_id, character_name)
        case _:
            await callback.message.answer("Invalid character type selected.")
            return

    if character is not None:
        kb = inline_keyboard(start_game="Start Journey")
        await character.save_character_state()
        await callback.message.answer("You character was saved", reply_markup=kb)
        await callback.answer()
