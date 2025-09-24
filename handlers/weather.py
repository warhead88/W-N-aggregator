from aiogram import Router, types
from aiogram.filters import Command

from datetime import datetime

from services import weather

router = Router()

@router.message(Command("weather"))
async def get_weather(message: types.Message):
    text = message.text.split()
    if len(text) == 2:
        city = text[1]
    else:
        await message.answer("Введите команду в корректной форме.")
        return
    data = await weather.get_weather(city)

    name = data["name"]
    desc = data["weather"][0]["description"]
    temp = data["main"]["temp"]
    feels = data["main"]["feels_like"]
    t_min = data["main"]["temp_min"]
    t_max = data["main"]["temp_max"]
    humidity = data["main"]["humidity"]
    pressure = data["main"]["pressure"]

    wind_speed = data["wind"]["speed"]
    wind_deg = data["wind"]["deg"]
    gust = data["wind"].get("gust", 0)

    clouds = data["clouds"]["all"]
    
    if data["visibility"] < 1000:
        visibility = str(data["visibility"]) + " метров"
    else:
        visibility = str(data["visibility"] / 1000) + " километров"

    sunrise = datetime.fromtimestamp(data["sys"]["sunrise"]).strftime("%H:%M")
    sunset = datetime.fromtimestamp(data["sys"]["sunset"]).strftime("%H:%M")

    forecast = f"""🌍Город: {name},
☀️{desc},
🌡Температура: {temp} °C (ощущается как {feels} °C),
🔽Мин: {t_min} °C / 🔼Макс: {t_max} °C,
💧Влажность: {humidity} %,
🧭Давление: {pressure} гПа,
🌬Ветер: {wind_speed} m/s ({wind_deg}°), порывы до {gust} m/s,
☁️Облачность: {clouds} %,
👁Видимость: {visibility},
🌅Восход: {sunrise} / 🌇Закат: {sunset}."""

    await message.answer(forecast)
