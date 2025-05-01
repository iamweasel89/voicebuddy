# Используем официальный образ Python на базе Debian
FROM python:3.12-slim

# Устанавливаем зависимости
RUN apt-get update && apt-get install -y \
    portaudio19-dev \
    libffi-dev \
    git \
    curl \
    && apt-get clean

# Устанавливаем Python-зависимости проекта
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь проект в контейнер
COPY . /app
WORKDIR /app

# Создаём директорию под модели (если её ещё нет)
RUN mkdir -p models

# Указываем команду по умолчанию
CMD ["python", "core/raw_recognizer.py"]
