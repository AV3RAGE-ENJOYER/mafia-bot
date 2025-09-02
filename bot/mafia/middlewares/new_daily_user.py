import json

from redis.asyncio import Redis
# from confluent_kafka import Producer

class DailyUser:
    def __init__(self, redis: Redis, BOT_TYPE: str):
        self.redis = redis
        # self.kafka = kafka
        self.BOT_TYPE = BOT_TYPE

    async def __call__(self, handler, event, data):
        if not (await self.redis.sismember("daily_users", event.from_user.id)):
            await self.redis.sadd("daily_users", event.from_user.id)
            daily_users = await self.redis.smembers("daily_users")
            # self.kafka.produce(topic="daily_users", value=json.dumps({"bot_type": self.BOT_TYPE, "daily_users": len(daily_users)}).encode())

        return await handler(event, data)
