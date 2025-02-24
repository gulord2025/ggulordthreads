from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command
import asyncio
import logging
import os
from dotenv import load_dotenv
from aiogram import Router
import asyncpg
from fastapi import FastAPI
import uvicorn
import threading

# Загружаем переменные из файла gggulord.env
load_dotenv(dotenv_path="gggulord.env")

API_TOKEN = os.getenv("API_TOKEN")
ADMIN_ID = os.getenv("ADMIN_ID")
DATABASE_URL = os.getenv("DATABASE_URL")

if not API_TOKEN:
    print("❌ API_TOKEN не найден в .env файле!")
    exit()

if ADMIN_ID:
    try:
        ADMIN_ID = int(ADMIN_ID)
    except ValueError:
        print("❌ ADMIN_ID должен быть числом! Проверь .env файл.")
        exit()
else:
    print("❌ ADMIN_ID не найден в .env файле!")
    exit()

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher()
router = Router()

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

@router.message(Command("start"))
async def start(message: types.Message):
    user_id = message.from_user.id
    username = message.from_user.username

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

@router.message(Command("getid"))
async def getid(message: types.Message):
    if message.from_user.id == ADMIN_ID:
        async with db.acquire() as conn:
            users = await conn.fetch("SELECT user_id, username, message_count, clicked_buttons FROM users")
        if not users:
            await message.answer("⛔ В базе пока нет пользователей.")
            return
        response = "📊 **Список пользователей:**\n"
        for user in users:
            response += f"🆔 ID: {user['user_id']}, Username: @{user['username']}, Сообщений: {user['message_count']}, Кнопки: {user['clicked_buttons']}\n"
        await message.answer(response, parse_mode="Markdown")
    else:
        await message.answer("⛔ У вас нет доступа к этой команде.")

dp.include_router(router)

app = FastAPI()

@app.get("/")
def read_root():
    return {"status": "bot is running"}

def run_fastapi():
    uvicorn.run(app, host="0.0.0.0", port=8000)

async def main():
    await create_db_pool()
    print("✅ Бот запущен и готов к работе.")
    await dp.start_polling(bot)

if __name__ == "__main__":
    threading.Thread(target=run_fastapi, daemon=True).start()
    asyncio.run(main())
