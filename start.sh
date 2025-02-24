#!/bin/bash
# Устанавливаем необходимые зависимости
pip install -r requirements.txt

# Устанавливаем переменную окружения для порта (необязательно для работы, но требуется для Render)
export PORT=8000  # Указываем порт для FastAPI

# Запускаем FastAPI в фоне
python3 main.py &

# Запускаем бота
python3 ggulordthreads.py
