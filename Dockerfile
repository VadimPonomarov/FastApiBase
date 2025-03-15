FROM python:3.12-slim

# Устанавливаем переменные окружения
ENV PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем и устанавливаем зависимости отдельно
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Копируем файлы проекта
COPY . .

EXPOSE 8000
