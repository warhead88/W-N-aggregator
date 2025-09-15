import os
from dotenv import load_dotenv

load_dotenv()

class Config():
    BOT_TOKEN=os.getenv("BOT_TOKEN")
    NEWS_API=os.getenv("NEWS_API")
    WEATHER_API=os.getenv("WEATHER_API")
