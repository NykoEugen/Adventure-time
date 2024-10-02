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
    text = ("Base stats of characters: \n\n Warrior - The Warrior is a formidable melee fighter, "
            "renowned for their exceptional strength and endurance. "
            "Armed with heavy armor and a variety of weapons, they excel in close combat and can "
            "withstand significant damage: \n Strength - 15\n Dexterity - 10\n Intelligence - 5\n Endurance - 12\n "
            "Charisma - 6\n Health - depends on Endurance * 10\n Mana - depends on Intelligence * 10\n\n "
            "Mage - The Mage harnesses the power of magic to cast devastating spells, "
            "utilizing their high intelligence to manipulate elemental forces. "
            "With limited physical prowess, they rely on their magical abilities to deal damage from a "
            "distance and support their allies: \n Strength - 5\n Dexterity - 8\n Intelligence - 15\n Endurance - 6\n "
            "Charisma - 9\n Health - depends on Endurance * 10\n Mana - depends on Intelligence * 10\n\n "
            "Archer - The Archer is a master of ranged combat, skilled in precision and agility. "
            "With a keen eye and swift reflexes, they excel at taking down enemies from afar, "
            "using a combination of bows and specialized arrows to strike with deadly accuracy: \n Strength - 8\n "
            "Dexterity - 15\n Intelligence - 6\n Endurance - 10\n "
            "Charisma - 9\n Health - depends on Endurance * 10\n Mana - depends on Intelligence * 10\n ")
    await callback.message.answer(text)
    await asyncio.sleep(2)
    await callback.message.answer("Choose character type:", reply_markup=kb)
    await callback.answer()

@router.callback_query(lambda callback: callback.data in {"warrior", "mage", "archer"})
async def choose_character_type(callback: CallbackQuery, state: FSMContext):
    character_id = callback.from_user.id
    character_type = callback.data
    await state.update_data(character_type=character_type, character_id=character_id)
    await callback.message.answer("Create character name")
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
        await character.save_character_state()
        await callback.message.answer("You character was saved")
        await callback.answer()
