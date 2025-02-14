from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command
import asyncio
import logging
from aiogram import Router

API_TOKEN = "8181176657:AAFzf_yjbd6Np-SRd-E2hSTdKU1ZyNXiCuI"

# Логирование
logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher()
router = Router()

# Главное меню
@router.message(Command("start"))
async def start(message: types.Message):
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
        "Gulo Vision — это закрытое сообщество для тех, кто хочет прокачать свое мышление, научиться зарабатывать на своем контенте и масштабировать свои проекты. "
        "Здесь ты получаешь доступ к уникальной информации, разбору кейсов, личному опыту, а также поддержку сообщества единомышленников.\n\n"
        "**Структура недели:**\n"
        "🔹 *Понедельник* — Дисциплина и энергия\n"
        "Как правильно выстроить день, управлять ресурсами, сохранять мотивацию и становиться сильнее. Разбираем техники продуктивности и режимы, которые реально работают.\n\n"
        "🔹 *Вторник* — Блогерство и соцсети\n"
        "Как набрать миллионы подписчиков, создавать контент, который залетает, и делать так, чтобы алгоритмы работали на тебя.\n\n"
        "🔹 *Среда* — Бизнес и заработок\n"
        "Разбираем стратегии масштабирования и монетизации, кейсы успешных предпринимателей и возможности заработка в digital-сфере.\n\n"
        "🔹 *Четверг* — Мышление\n"
        "Глубокие разборы книг, концепций и стратегий, которые помогают лучше понимать мир, себя и законы успеха. Психология, философия, критическое мышление — всё, что делает тебя умнее и сильнее.\n\n"
        "🔹 *Пятница* — Групповые созвоны с Павлом Гуло\n"
        "Здесь ты можешь задать свои вопросы, получить личную обратную связь и обсудить самые актуальные темы недели.\n\n"
        "📢 *Бонус:*\n"
        "Участники получают доступ в общий закрытый чат, где можно обмениваться идеями, получать советы и находить единомышленников.\n\n"
        "Gulo Vision — это не просто закрытый канал, а экосистема для роста, где ты становишься частью движения.\n\n"
        "🔗 [Оплатить через Lava.top](https://linktw.in/SiXwAI)",
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

# Регистрация роутера
dp.include_router(router)

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
