#!/bin/bash
pip install -r requirements.txt

# Запускаем FastAPI в фоне
uvicorn main:app --host 0.0.0.0 --port 8000 &

# Запускаем бота
python3 main.py
