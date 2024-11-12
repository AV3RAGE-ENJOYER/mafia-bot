import os
import random
import json

from confluent_kafka import Producer

from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery, FSInputFile

from mafia.config import BOT_TYPE
from mafia.keyboard.client_keyboard import kb_client, kb_rules, kb_roles, kb_buy, kb_check_menu, kb_game
from mafia.database.controller import PostgresDatabase

client_router = Router()

@client_router.message(CommandStart())
@client_router.message(Command("help"))
async def message_handler(message: Message, responses: dict, db: PostgresDatabase, kafka: Producer):
    res = f"Привет, {message.from_user.first_name}! Я чат бот по игре: Магфия ✨🧙‍♂️ Я помогу тебе разобраться в правилах игры, расскажу много интересного о вселенной Гарри Поттера, чтобы познакомить с миром волшебства и сделать твой игровой процесс незабываемым ଘ(∩^o^)⊃━☆\nС чего начнем ?"

    await message.answer(text=res, reply_markup=kb_client)
    
    await message.answer_sticker(
        sticker="CAACAgIAAxkBAAEKAolk2QKfqiwBdcpNK0oqU2Y5Mnrm2QACzQIAAs9fiwdR72f8Nh_oNjAE"
    )

@client_router.message(F.text == "Сюжет")
async def tell_the_plot(message: Message, responses: dict):
    await message.answer_photo(FSInputFile(f"{os.getcwd()}/handlers/images/{BOT_TYPE}/fight.jpg"),
        caption=responses["tell_the_plot"], reply_markup=kb_client)

@client_router.message(F.text == "Ход игры")
async def tell_the_rules(message: Message, responses: dict):
    await message.answer(text=responses["tell_the_rules"], reply_markup=kb_rules)

@client_router.message(F.text == "Роли")
async def roles(message: Message, responses: dict):
    await message.answer(text=responses["roles"], reply_markup=kb_roles)

@client_router.message(F.text == "Ночь")
async def night_rules(message: Message, responses: dict):
    await message.answer_photo(FSInputFile(f"{os.getcwd()}/handlers/images/{BOT_TYPE}/night.jpg"))
    await message.answer(text=responses["night_rules"])

@client_router.message(F.text == "Утро")
async def wake_up(message: Message, responses: dict):
    await message.answer_photo(FSInputFile(f"{os.getcwd()}/handlers/images/{BOT_TYPE}/wake_up.jpg"),
        caption=responses["wake_up"])

@client_router.message(F.text == "Дневные голосования")
async def take_votes(message: Message, responses: dict):
    await message.answer_photo(FSInputFile(f"{os.getcwd()}/handlers/images/{BOT_TYPE}/vote.jpg"),
        caption=responses["take_votes"])

@client_router.message(F.text == "Назад")
async def exit_button(message: Message):
    await message.answer_sticker(
        sticker="CAACAgIAAxkBAAEKA9tk2cNtGxZbQIPZlJdFD8RP1VHebAAC6QIAAs9fiwcDv7hfUN45vTAE",
        reply_markup=kb_client
    )

@client_router.message(F.text == "Купить магфию")
async def buy_game(message: Message, responses: dict):
    await message.answer(text=responses["buy_game"], reply_markup=kb_buy)

@client_router.message(F.text == "Челленджи")
async def beans(message: Message, responses: dict):
    await message.answer(text=responses["beans"], reply_markup=kb_game)

@client_router.message(F.text == "Рандомное задание")
async def challenges(message: Message, responses: dict):
    await message.answer(
        responses["game_options"][random.randint(0, len(responses["game_options"]) - 1)])

# CALLBACK

@client_router.callback_query(F.data == "sub_done")
async def call_check(callback: CallbackQuery, responses: dict):
    res = f"Привет, {callback.from_user.first_name}! Я чат бот по игре: Магфия ✨🧙‍♂️ Я помогу тебе разобраться в правилах игры, расскажу много интересного о вселенной Гарри Поттера, чтобы познакомить с миром волшебства и сделать твой игровой процесс незабываемым ଘ(∩^o^)⊃━☆\nС чего начнем ?"

    await callback.message.answer(text=res, reply_keyboard=kb_client)
    await callback.message.answer_sticker(
        sticker="CAACAgIAAxkBAAEKAolk2QKfqiwBdcpNK0oqU2Y5Mnrm2QACzQIAAs9fiwdR72f8Nh_oNjAE"
    )

roles = ["vil", "her", "doc", "dl", "dem", "bad", "pri", "pol", "aut"]

@client_router.callback_query(F.data.in_(roles))
async def callback_handler(callback: CallbackQuery, responses: dict):
    await callback.message.answer_photo(
        FSInputFile(f"{os.getcwd()}/handlers/images/{BOT_TYPE}/{callback.data}.jpg"),
        caption=responses[callback.data], reply_markup=kb_roles)