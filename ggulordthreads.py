from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command
import asyncio
import logging
import os
from dotenv import load_dotenv
from aiogram import Router

# Загружаем переменные из файла gggulord.env
load_dotenv(dotenv_path="gggulord.env")

# Получаем токен и ID администратора из переменных окружения
API_TOKEN = os.getenv("API_TOKEN")
ADMIN_ID = os.getenv("ADMIN_ID")

# Проверка, что токен успешно загружен
if not API_TOKEN:
    print("API_TOKEN не найден в .env файле!")
    exit()

# Логирование
logging.basicConfig(level=logging.INFO)

# Инициализация бота
bot = Bot(token=API_TOKEN)
dp = Dispatcher()
router = Router()

# Главное меню
@router.message(Command("start"))
async def start(message: types.Message):
    user_id = message.from_user.id
    keyboard = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="Гайд"), KeyboardButton(text="Gulo Vision")]],
        resize_keyboard=True
    )
    await message.answer(
        "Добро пожаловать в бота GGulord Vision!\n\n"
        "Нажмите кнопку \"Гайд\", чтобы получить бесплатный гайд.\n"
        "Нажмите \"Gulo Vision\", чтобы узнать больше о закрытом сообществе.",
        reply_markup=keyboard
    )

# Гайд
@router.message(lambda message: message.text == "Гайд")
async def send_guide(message: types.Message):
    keyboard = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="Назад"), KeyboardButton(text="Помощь")]],
        resize_keyboard=True
    )
    await message.answer(
        "Спасибо за ваш интерес к блогерству и саморазвитию!\n\n"
        "📘 [Гайд](https://docs.google.com/presentation/d/1kWBBM4I_wArYXtGrp0SwtmiFVj1uxwLfMTVtIu3RGYM/edit?usp=sharing)",
        parse_mode="Markdown",
        reply_markup=keyboard
    )

# Gulo Vision
@router.message(lambda message: message.text == "Gulo Vision")
async def send_gulo_vision_info(message: types.Message):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Оплатить", url="https://linktw.in/SiXwAI")],
            [InlineKeyboardButton(text="Кейсы Павла Гуло", url="https://t.me/+8XvQcRpxKMc4MGRi")],
            [InlineKeyboardButton(text="Помощь", url="https://t.me/pavel_gulo")]
        ]
    )
    await message.answer(
        "🔹 **Что такое Gulo Vision?**\n\n"
        "Gulo Vision — это закрытое сообщество для тех, кто хочет прокачать свое мышление, научиться зарабатывать на своем контенте и масштабировать свои проекты."
        "\n\n🔗 [Оплатить через Lava.top](https://linktw.in/SiXwAI)",
        parse_mode="Markdown",
        reply_markup=keyboard
    )

# Помощь
@router.message(lambda message: message.text == "Помощь")
async def help_command(message: types.Message):
    await message.answer("Свяжитесь с поддержкой: @pavel_gulo")

# Назад
@router.message(lambda message: message.text == "Назад")
async def back_to_main(message: types.Message):
    await start(message)

# Статистика
@router.message(Command("stats"))
async def stats(message: types.Message):
    if message.from_user.id == int(ADMIN_ID):
        await message.answer(f"Количество уникальных пользователей: {len(set())}")
    else:
        await message.answer("У вас нет доступа к статистике.")

# Регистрация роутера
dp.include_router(router)

# Запуск бота
async def main():
    # Запуск бота
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
