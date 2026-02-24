import os
from dotenv import load_dotenv

load_dotenv()

class Config():
    BOT_TOKEN=os.getenv("BOT_TOKEN")
    NEWS_API=os.getenv("NEWS_API")
    WEATHER_API=os.getenv("WEATHER_API")

    POSTGRES_USER=os.getenv("POSTGRES_USER", "postgres")
    POSTGRES_PASSWORD=os.getenv("POSTGRES_PASSWORD", "postgres")
    POSTGRES_DB=os.getenv("POSTGRES_DB", "main_db")
    POSTGRES_HOST=os.getenv("POSTGRES_HOST", "localhost")
    POSTGRES_PORT=os.getenv("POSTGRES_PORT", "5432")
