from dotenv import load_dotenv
import os

load_dotenv("config.env")

BOT_TYPE=os.getenv("BOT_TYPE")
BOT_TOKEN=os.getenv("BOT_TOKEN")
CHANNEL_ID=os.getenv("CHANNEL_ID")
REDIS_HOST=os.getenv("REDIS_HOST")
POSTGRES_URL=os.getenv("POSTGRES_URL")