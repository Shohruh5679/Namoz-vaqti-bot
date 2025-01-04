import requests
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from datetime import datetime
import asyncio



bot = Bot(token="BOT TOKEN")
dp = Dispatcher()

API_URL = "http://api.aladhan.com/v1/timingsByCity"


def get_prayer_times(city: str):
    today = datetime.today().strftime('%Y-%m-%d')
    params = {
        "city": city,
        "country": "Uzbekistan",
        "method": 2,
        "date": today
    }
    response = requests.get(API_URL, params=params)
    data = response.json()

    if data['code'] == 200:
        timings = data['data']['timings']
        return timings
    else:
        return None


@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("Salom! Namoz vaqti botiga xush kelibsiz. Iltimos, shahar nomini kiriting.")


# Namoz vaqtlari uchun funksiya
@dp.message()
async def get_prayers(message: types.Message):
    city_name = message.text.strip()
    timings = get_prayer_times(city_name)

    if timings:
        response = (
            f"Namoz vaqtlari ({city_name}):\n"
            f"Bomdod: {timings['Fajr']}\n"
            f"Quyosh: {timings['Dhuhr']}\n"
            f"Asr: {timings['Asr']}\n"
            f"Shom: {timings['Maghrib']}\n"
            f"Isha: {timings['Isha']}\n"
        )
        await message.answer(response)
    else:
        await message.answer("Iltimos, shahar nomini to'g'ri kiriting.")


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
