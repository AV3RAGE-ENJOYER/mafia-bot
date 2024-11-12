from redis.asyncio import Redis

from aiogram import Router, F, Bot
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from mafia.database.controller import PostgresDatabase
from mafia.filters.admin import AdminFilter
from mafia.keyboard.admin_keyboard import kb_admin, kb_admin_cancel, kb_admin_confirm

class MaillingState(StatesGroup):
    text = State()
    confirm = State()

admin_router = Router()

@admin_router.message(Command("admin"), AdminFilter())
async def admin_panel(message: Message):
    await message.answer(text="Добро пожаловать в админ панель!", reply_markup=kb_admin)

@admin_router.message(F.text == "Создать рассылку", AdminFilter())
async def create_mailing(message: Message, state: FSMContext):
    await state.set_state(MaillingState.text)
    await message.answer(text="Введите текст рассылки:", reply_markup=kb_admin_cancel)

@admin_router.message(F.text == "Отмена", AdminFilter())
async def cancel(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(text="Рассылка отменена", reply_markup=kb_admin)

@admin_router.message(MaillingState.text, AdminFilter())
async def mailling_text(message: Message, state: FSMContext):
    await state.update_data(text=message.text)
    await state.set_state(MaillingState.confirm)
    await message.answer(text="Вы уверены, что хотите разослать это сообщение всем пользователям?", reply_markup=kb_admin_confirm)

@admin_router.message(MaillingState.confirm, AdminFilter())
async def confirm(message: Message, state: FSMContext, db: PostgresDatabase, bot: Bot):
    if message.text == "Да":
        await message.answer("Рассылка создана", reply_markup=kb_admin)
        mailling_text = await state.get_value("text")

        for user in db.get_users():
            try:
                await bot.send_message(chat_id=user.id, text=mailling_text)
            except:
                # User restricted messages
                pass
        await state.clear()
        return
    
    await message.answer(text="Вы уверены, что хотите разослать это сообщение всем пользователям?", reply_markup=kb_admin_confirm)

@admin_router.message(F.text == "Посмотреть статистику", AdminFilter())
async def show_statistics(message: Message, db: PostgresDatabase, redis: Redis):
    users = db.get_users()
    daily_users = await redis.smembers("daily_users")

    oldest_user = min(users)
    newest_user = max(users)

    res = f"👥 Количество пользователей: {len(users)}\n👥 Количество пользователей за день: {len(daily_users)}\n\n👴🏻 Самый старый пользователь: @{oldest_user.username} ({oldest_user.convert_to_date()})\n👱‍♂️ Самый новый пользователь: @{newest_user.username} ({newest_user.convert_to_date()})"
    
    await message.answer(
        text=res, 
        reply_markup=kb_admin)