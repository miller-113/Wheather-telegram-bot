import math
import random

import requests
import datetime

from config import open_weather_token, tg_bot_token
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

bot = Bot(token=tg_bot_token)  # Your telegram Token
dp = Dispatcher(bot)

main_button = KeyboardButton('Main')
time_button = KeyboardButton('Data time')
random_number = KeyboardButton('Random number')
other_button = KeyboardButton('Other')
main_menu = ReplyKeyboardMarkup(resize_keyboard=True).add(time_button, random_number, other_button)

currency_button = KeyboardButton('Currency')
inf_button = KeyboardButton('Information')
other_menu = ReplyKeyboardMarkup(resize_keyboard=True).add(currency_button, inf_button, main_button)


@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    await message.reply('Привет, напиши название своего города и я пришлю погоду!\n\n \help for more commands')


@dp.message_handler(commands=['help'])
async def help_commands(message: types.Message):
    await message.reply(f'List commands:\n/DataTime\n/RandomNumber\n/Currency\n/Information', reply_markup=main_menu)

@dp.message_handler(commands=['DataTime'])
async def help_commands(message: types.Message):
    await message.reply(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))


currency_list = requests.get('https://api.privatbank.ua/p24api/pubinfo?exchange&json&coursid=5').json()

new_list = []
for i in currency_list:
    new_list.append(i.get('ccy'))
    new_list.append(i.get('buy'))

x = '*' * 15

@dp.message_handler()
async def get_weather(message: types.Message):
    # if message.text == 'DataTime':
    #     await message.reply(f"datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')")
    if message.text == 'Main':
        await bot.send_message(message.from_user.id, 'Main menu', reply_markup=main_menu)
    elif message.text == 'Other':
        await bot.send_message(message.from_user.id, 'Other menu', reply_markup=other_menu)
    elif message.text == 'Information':
        await bot.send_message(message.from_user.id, 'Information text:')
    elif message.text == 'RandomNumber':
        await bot.send_message(message.from_user.id, str(random.randint(0, 1000)))
    elif message.text == 'Currency':
        await bot.send_message(message.from_user.id, f'{new_list[0]}\n {new_list[1]}\n{x}\n'
                                                     f'{new_list[2]}\n {new_list[3]}\n{x}\n'
                                                     f'{new_list[4]}\n {new_list[5]}')
    else:
        smile_code = {"Clear": "Ясно\u2060",
                      'Clouds': "Облачно\u2601",
                      'Rain': "Дождь\u2614",
                      'Drizzle': "Дождь\u2614",
                      'Thunderstorm': "Гроза\u2614",
                      'Snow': "Снег\u2614",
                      'Mist': "Туман\u2614",
                      }
        try:
            r = requests.get(
                f'https://api.openweathermap.org/data/2.5/weather?q={message.text}&appid={open_weather_token}',
                # Your Token
                params={"units": "metric"})
            data = r.json()

            weather_description = data['weather'][0]['main']
            if weather_description in smile_code:
                wd = smile_code[weather_description]
            else:
                pass

            city = data['name']
            cur_weather = data['main']['temp']
            cur_humidity = data['main']['humidity']
            cur_pressure = data['main']['pressure']
            wind = data['wind']['speed']

            sunrise_timestamp = datetime.datetime.fromtimestamp(data['sys']['sunrise'])
            sunset_timestamp = datetime.datetime.fromtimestamp(data['sys']['sunset'])
            len_of_day = sunset_timestamp - sunrise_timestamp

            await message.reply(f'{datetime.datetime.now().strftime("%Y-%m-%d %H:%M")}\n'
                                f'Погода в городе: {city}\nТемпература: {math.ceil(cur_weather)}\u2103 {wd}\n'
                                f'Влажность: {cur_humidity}%\nДавление: {cur_pressure}мм.рт.ст.\n'
                                f'Ветер: {wind}м/с\nВосход солнца: {sunrise_timestamp}\n'
                                f'Закат солнца: {sunset_timestamp}\n'
                                f'Продолжительность дня: {len_of_day}\n'
                                f'Хорошего дня!')
        except:
            await message.reply('Проверьте название города или команда /help')


if __name__ == '__main__':
    executor.start_polling(dp)
