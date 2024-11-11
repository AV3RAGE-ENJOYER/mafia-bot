from aiogram.filters import BaseFilter
from aiogram.types import Message

from mafia.database.controller import PostgresDatabase

class AdminFilter(BaseFilter):

    async def __call__(self, message: Message, db: PostgresDatabase) -> bool:
        return db.check_admin(message.from_user.id) 