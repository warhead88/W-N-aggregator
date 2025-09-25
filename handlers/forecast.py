from aiogram import Router, types
from aiogram.filters import Command

from datetime import datetime
from collections import defaultdict

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
    
    data = await weather.get_forecast(city)

    forecast_by_day = defaultdict(lambda: {"temps": [], "descriptions": []})
    
    for entry in data["list"]:
        dt_txt = entry["dt_txt"]
        date_str = dt_txt.split(" ")[0]
    
        temp = entry["main"]["temp"]
        desc = entry["weather"][0]["description"]

        forecast_by_day[date_str]["temps"].append(temp)
        forecast_by_day[date_str]["descriptions"].append(desc)

    dates = sorted(forecast_by_day.keys())[:3]

    text = ""

    for d in dates:
        temps = forecast_by_day[d]["temps"]
        descs = forecast_by_day[d]["descriptions"]

        avg_temp = sum(temps) / len(temps)
        min_temp = min(temps)
        max_temp = max(temps)

        main_desc = max(set(descs), key=descs.count)

        day = datetime.strptime(d, "%Y-%m-%d").strftime("%d.%m.%Y")

        text = text + f"<b>{day}</b>: {main_desc}, {avg_temp:.1f}°C (от {min_temp:.1f} до {max_temp:.1f})\n\n"

    await message.answer(text, parse_mode="HTML")
