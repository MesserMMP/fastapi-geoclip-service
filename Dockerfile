FROM python:3.10-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файл с зависимостями и устанавливаем их
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем код приложения
COPY app/ ./app

# Открываем порт для FastAPI
EXPOSE 8000

# Команда запуска приложения
CMD ["python", "app/main.py"]
