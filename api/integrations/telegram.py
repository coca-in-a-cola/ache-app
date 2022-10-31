import asyncio
import logging
import aiogram.utils.executor
from aiogram import Bot, Dispatcher, types
from aiogram.types import WebAppInfo
import textwrap

logging.basicConfig(level=logging.INFO)
bot = Bot(token="5437913533:AAGPXEDnAbsqxG4bna7aphbdXbBIXE76twA")
dp = Dispatcher(bot)
web_app_1 = WebAppInfo(url='https://chromedino.com')

@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup()
    message.from_user.id
    button_1 = types.KeyboardButton(text="назначить встречу", web_app=web_app_1)
    keyboard.add(button_1) #button_2)
    await bot.send_message(message.chat.id, \
        textwrap.dedent(f"""
        Приветствую тебя {message.from_user.full_name}!")
        """), reply_markup=keyboard)

aiogram.utils.executor.start_polling(dp)