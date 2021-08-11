FROM python:3.8

# Задаем переменные окружения
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1  # Не создаем .pyc файлы

# Установка зависимостей
RUN apt-get update \
    && apt-get install netcat -y
RUN apt-get upgrade -y && apt-get install gcc python3-dev musl-dev -y
RUN pip install --upgrade pip

WORKDIR /app
RUN mkdir static
RUN mkdir media

COPY requirements.txt .
RUN pip install -r requirements.txt
COPY app .
