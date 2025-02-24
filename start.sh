#!/bin/bash
# Устанавливаем необходимые зависимости
pip install -r requirements.txt

# Устанавливаем переменную окружения для порта (Render требует её)
export PORT=8000  

# Запускаем FastAPI и бота в фоне
python3 main.py &
python3 ggulordthreads.py
