import requests
import datetime
from aiogram import Bot,types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

owm = '7b659fb4cce20f478cd700bcffcfa5d3'
bot = Bot(token='5395672939:AAEqRuFC42hoqZJQFg_xijgVwqrRLPZv7t0')
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def start_command(message:types.Message):
    await message.reply('Привет! Напиши мне свой город, а я расскажу о погоде')


@dp.message_handler()
async def get_weather(message:types.Message):
    code_to_smile = {
        "Clear": "Ясно \U00002600",
        "Clouds": "Облачно \U00002601",
        "Rain": "Дождь \U00002614",
        "Drizzle": "Дождь \U00002614",
        "Thunderstorm": "Гроза \U000026A1",
        "Snow": "Снег \U0001F328",
        "Mist": "Туман \U0001F32B",
    }

    try:
        r = requests.get(
            f"http://api.openweathermap.org/data/2.5/weather?q={message.text}&appid={owm}&units=metric"
        )
        data = r.json()


        city = data["name"]
        cur_weather = data["main"]["temp"]

        weather_description = data["weather"][0]["main"]
        if weather_description in code_to_smile:
            wd = code_to_smile[weather_description]
        else:
            wd = "Посмотри в окно, не пойму что там за погода!"

        feels_like = data["main"]["feels_like"]
        sunrise_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunrise"])
        sunset_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunset"])

        await message.reply(f"*** {datetime.datetime.now().strftime('%d/%m/%y %H:%M')} ***\n"
              f'Погода в городе : {city}\nТемпература : {cur_weather}C°{wd}\n'
              f'Ощущается как : {feels_like}C°\n'
              f'Восход солнца : {sunrise_timestamp}\n'
              f'Закат солнца : {sunset_timestamp}\n'
              f'Хорошего дня!'
              )

    except :
        await message.reply('Проверьте верно ли введено название города')


if __name__ == '__main__':
    executor.start_polling(dp)



