from aiogram import Router, types
from aiogram.filters import Command

from datetime import datetime
from collections import defaultdict
import html

from services import weather

router = Router()

@router.message(Command("forecast"))
async def get_forecast(message: types.Message):
    text = message.text.split()
    if len(text) == 2:
        city = text[1]
    else:
        await message.answer("Введите команду в корректной форме.")
        return
    
    safe_city = html.escape(city)
    
    try:
        data = await weather.get_forecast(city)
    except Exception as e:
        await message.answer(f"Не удалось получить прогноз для <b>{safe_city}</b>.", parse_mode="HTML")
        return

    forecast_by_day = defaultdict(lambda: {"temps": [], "descriptions": []})
    
    for entry in data.get("list", []):
        dt_txt = entry.get("dt_txt", "")
        if not dt_txt:
            continue
        date_str = dt_txt.split(" ")[0]
    
        temp = entry.get("main", {}).get("temp", 0)
        desc = entry.get("weather", [{}])[0].get("description", "Нет данных")

        forecast_by_day[date_str]["temps"].append(temp)
        forecast_by_day[date_str]["descriptions"].append(desc)

    dates = sorted(forecast_by_day.keys())[:3]

    response_text = ""

    for d in dates:
        temps = forecast_by_day[d]["temps"]
        descs = forecast_by_day[d]["descriptions"]

        if not temps:
            continue

        avg_temp = sum(temps) / len(temps)
        min_temp = min(temps)
        max_temp = max(temps)

        main_desc = max(set(descs), key=descs.count)

        day = datetime.strptime(d, "%Y-%m-%d").strftime("%d.%m.%Y")

        response_text += f"<b>{day}</b>: {main_desc}, {avg_temp:.1f}°C (от {min_temp:.1f} до {max_temp:.1f})\n\n"

    if not response_text:
        response_text = "Прогноз не найден."

    await message.answer(response_text, parse_mode="HTML")
