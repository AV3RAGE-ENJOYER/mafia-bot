import asyncio
import logging
import sys
import config
import socket

from redis.asyncio import Redis
from confluent_kafka import Producer

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.redis import RedisStorage

from responses import responses
from handlers import client, admin
from middlewares.add_user import AddUser
from middlewares.new_daily_user import DailyUser
from middlewares.check_subscription import SubscriptionMiddleware
from database.controller import PostgresDatabase

redis_conn = Redis(host=config.REDIS_HOST, decode_responses=True)
postgres_db = PostgresDatabase(config.POSTGRES_URL)

kafka_producer = Producer(
    {
        'bootstrap.servers': 'kafka:29092', 
        'client.id': socket.gethostname()
    }
)

bot = Bot(token=config.BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

dp = Dispatcher(
    storage=RedisStorage(redis_conn), 
    responses=responses[config.BOT_TYPE],
    redis=redis_conn, 
    db=postgres_db
)

async def main() -> None:
    user_count = postgres_db.count_users()

    if user_count == None:
        user_count = 0

    await redis_conn.set("user_count", user_count)

    dp.include_routers(
        client.client_router,
        admin.admin_router
    )
    
    dp.message.middleware(AddUser(db=postgres_db, BOT_TYPE=config.BOT_TYPE))
    dp.message.middleware(SubscriptionMiddleware(bot, config.CHANNEL_ID))
    dp.callback_query.middleware(SubscriptionMiddleware(bot, config.CHANNEL_ID))
    dp.message.middleware(DailyUser(redis=redis_conn, BOT_TYPE=config.BOT_TYPE))

    await dp.start_polling(bot)
    
    postgres_db.close()

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())