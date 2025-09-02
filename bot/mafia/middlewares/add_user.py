import json

from mafia.database.controller import PostgresDatabase
# from confluent_kafka import Producer

class AddUser:
    def __init__(self, db: PostgresDatabase, BOT_TYPE):
        self.db = db
        # self.kafka = kafka
        self.BOT_TYPE = BOT_TYPE

    async def __call__(self, handler, event, data):
         
        if not self.db.check_user(event.from_user.id):
            self.db.add_user(event.from_user.id, event.from_user.username)

            user_count = self.db.count_users()
            # self.kafka.produce(topic="users", value=json.dumps({"bot_type": self.BOT_TYPE, "user_count": user_count}).encode())


        return await handler(event, data)