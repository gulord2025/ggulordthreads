from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
import asyncpg
import asyncio

TOKEN = "ТВОЙ_ТОКЕН_БОТА"
ADMIN_ID = 123456789  # Укажи свой Telegram ID

# Подключение к БД
async def create_db():
    return await asyncpg.create_pool(
        database="tg_bot_db",
        user="your_user",
        password="your_password",
        host="localhost"
    )

# Бот и диспетчер
bot = Bot(token=TOKEN, parse_mode="HTML")
dp = Dispatcher()
db = None  # База данных (инициализируется позже)

# Главное меню
main_keyboard = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="Гайд"), KeyboardButton(text="Gulo Vision")]],
    resize_keyboard=True
)

# Функция старта
@dp.message(Command("start"))
async def start_command(message: types.Message):
    await message.answer("Привет! Добро пожаловать в бота.", reply_markup=main_keyboard)

# Обработчик кнопки "Гайд"
@dp.message(lambda message: message.text == "Гайд")
async def send_guide(message: types.Message):
    guide_keyboard = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="Назад"), KeyboardButton(text="Помощь")]],
        resize_keyboard=True
    )
    await message.answer(
        "Спасибо за ваш интерес к блогерству и саморазвитию!\n\n"
        "📘 Гайд: [Перейти к гайду](https://docs.google.com/presentation/d/1kWBBM4I_wArYXtGrp0SwtmiFVj1uxwLfMTVtIu3RGYM/edit?usp=sharing)",
        reply_markup=guide_keyboard,
        parse_mode="Markdown"
    )

# Обработчик кнопки "Помощь"
@dp.message(lambda message: message.text and "Помощь" in message.text)
async def help_command(message: types.Message):
    await message.answer("🤖 Поддержка: [Связаться](https://t.me/pavel_gulo)", parse_mode="Markdown")

# Обработчик кнопки "Назад"
@dp.message(lambda message: message.text and "Назад" in message.text)
async def back_to_main(message: types.Message):
    await message.answer("🔙 Вы вернулись в главное меню.", reply_markup=main_keyboard)

# Команда /getid (только для ADMIN_ID)
@dp.message(Command("getid"))
async def getid(message: types.Message):
    if message.from_user.id == ADMIN_ID:
        async with db.acquire() as conn:
            users = await conn.fetch("SELECT user_id, username, message_count, clicked_buttons FROM users")
        
        if not users:
            await message.answer("⛔ В базе пока нет пользователей.")
            return

        response = "📊 **Список пользователей:**\n"
        for user in users:
            response += f"🆔 ID: `{user['user_id']}`, Username: @{user['username']}, Сообщений: {user['message_count']}, Кнопки: `{user['clicked_buttons']}`\n\n"

        await message.answer(response, parse_mode="Markdown")
    else:
        await message.answer("⛔ У вас нет доступа к этой команде.")

# Запуск бота
async def main():
    global db
    db = await create_db()
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
