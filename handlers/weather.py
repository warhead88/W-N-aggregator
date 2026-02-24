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
    import html
    safe_city = html.escape(city)

    try:
        data = await weather.get_weather(city)
    except Exception as e:
        await message.answer(f"Не удалось получить погоду для <b>{safe_city}</b>. Проверьте правильность названия города.", parse_mode="HTML")
        return

    name = html.escape(data.get("name", city))
    weather_desc = data.get("weather", [{}])[0].get("description", "Нет данных")
    main = data.get("main", {})
    temp = main.get("temp", "N/A")
    feels = main.get("feels_like", "N/A")
    t_min = main.get("temp_min", "N/A")
    t_max = main.get("temp_max", "N/A")
    humidity = main.get("humidity", "N/A")
    pressure = main.get("pressure", "N/A")
    wind = data.get("wind", {})
    wind_speed = wind.get("speed", "N/A")
    wind_deg = wind.get("deg", "N/A")
    gust = wind.get("gust", 0)
    clouds = data.get("clouds", {}).get("all", "N/A")
    vis = data.get("visibility", 0)

    if vis < 1000:
        visibility = f"{vis} метров"
    else:
        visibility = f"{vis / 1000} километров"

    sys_data = data.get("sys", {})
    sunrise = datetime.fromtimestamp(sys_data.get("sunrise", 0)).strftime("%H:%M") if sys_data.get("sunrise") else "N/A"
    sunset = datetime.fromtimestamp(sys_data.get("sunset", 0)).strftime("%H:%M") if sys_data.get("sunset") else "N/A"

    forecast = f"""🌍Город: {name},
☀️{weather_desc},
🌡Температура: {temp} °C (ощущается как {feels} °C),
🔽Мин: {t_min} °C / 🔼Макс: {t_max} °C,
💧Влажность: {humidity} %,
🧭Давление: {pressure} гПа,
🌬Ветер: {wind_speed} m/s ({wind_deg}°), порывы до {gust} m/s,
☁️Облачность: {clouds} %,
👁Видимость: {visibility},
🌅Восход: {sunrise} / 🌇Закат: {sunset}."""

    await message.answer(forecast)
