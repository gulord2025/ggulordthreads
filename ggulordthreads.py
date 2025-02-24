from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command
import asyncio
import logging
import os
from dotenv import load_dotenv
from aiogram import Router
import asyncpg

# Загружаем переменные из файла gggulord.env
load_dotenv(dotenv_path="gggulord.env")

# Получаем токен и ID администратора из переменных окружения
API_TOKEN = os.getenv("API_TOKEN")
ADMIN_ID = os.getenv("ADMIN_ID")
DATABASE_URL = os.getenv("DATABASE_URL")

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

# Подключение к базе данных
db = None

async def create_db_pool():
    global db
    db = await asyncpg.create_pool(DATABASE_URL)
    async with db.acquire() as conn:
        await conn.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                user_id BIGINT UNIQUE NOT NULL,
                username TEXT,
                message_count INT DEFAULT 0,
                clicked_buttons TEXT DEFAULT ''
            )
        """)
        print("✅ База данных подключена и таблица создана (если её не было).")

# Главное меню
@router.message(Command("start"))
async def start(message: types.Message):
    user_id = message.from_user.id
    username = message.from_user.username

    # Сохраняем пользователя в базу
    async with db.acquire() as conn:
        await conn.execute("""
            INSERT INTO users (user_id, username) VALUES ($1, $2)
            ON CONFLICT (user_id) DO NOTHING
        """, user_id, username)

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

# Логирование сообщений
@router.message()
async def log_message(message: types.Message):
    user_id = message.from_user.id
    text = message.text

    async with db.acquire() as conn:
        await conn.execute("""
            UPDATE users SET message_count = message_count + 1, 
            clicked_buttons = clicked_buttons || $1 || ',' 
            WHERE user_id = $2
        """, text, user_id)

# Помощь
@router.message(lambda message: message.text == "Помощь")
async def help_command(message: types.Message):
    await message.answer("Свяжитесь с поддержкой: @pavel_gulo")

# Назад
@router.message(lambda message: message.text == "Назад")
async def back_to_main(message: types.Message):
    await start(message)

# Получение ID пользователей
@router.message(Command("getid"))
async def getid(message: types.Message):
    if message.from_user.id == int(ADMIN_ID):
        async with db.acquire() as conn:
            users = await conn.fetch("SELECT user_id, username, message_count, clicked_buttons FROM users")
        
        response = "📊 Список пользователей:\n"
        for user in users:
            response += f"ID: {user['user_id']}, Username: {user['username']}, Сообщений: {user['message_count']}, Кнопки: {user['clicked_buttons']}\n"
        
        await message.answer(response)
    else:
        await message.answer("У вас нет доступа к этой команде.")

# Регистрация роутера
dp.include_router(router)

# Запуск бота
async def main():
    await create_db_pool()  # Подключение к базе перед стартом бота
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
