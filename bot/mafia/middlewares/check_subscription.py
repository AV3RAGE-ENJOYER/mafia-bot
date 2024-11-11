from aiogram import Bot
from aiogram.types.chat_member_left import ChatMemberLeft
from mafia.keyboard.client_keyboard import kb_check_menu

class SubscriptionMiddleware:
    def __init__(self, bot: Bot, channel_id):
        self.bot = bot
        self.channel_id = channel_id

    async def __call__(self, handler, event, data):
        member = await self.bot.get_chat_member(chat_id=self.channel_id, user_id=event.from_user.id)

        if isinstance(member, ChatMemberLeft):
            await self.bot.send_message(
                event.from_user.id,
                text="Для получения доступа к функционалу бота, пожалуйста, подпишитесь на канал !",
                reply_markup=kb_check_menu
            )
            return
        
        return await handler(event, data)