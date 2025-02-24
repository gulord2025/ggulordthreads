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
        "Добро пожаловать в бота GGulord Vision!", reply_markup=keyboard
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

# Регистрация роутера
dp.include_router(router)

# FastAPI сервер для Render
app = FastAPI()
@app.get("/")
def read_root():
    return {"status": "bot is running"}

async def main():
    await create_db_pool()
    await dp.start_polling(bot)

def run_fastapi():
    uvicorn.run(app, host="0.0.0.0", port=8000)

if __name__ == "__main__":
    threading.Thread(target=run_fastapi, daemon=True).start()
    asyncio.run(main())
