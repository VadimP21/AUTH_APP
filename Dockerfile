# Используем официальный образ Python
FROM python:3.8-slim

# Устанавливаем переменную окружения для Python
ENV PYTHONUNBUFFERED 1

# Создаем и переходим в директорию /code
RUN mkdir /app
WORKDIR /app

# Копируем файл зависимостей и устанавливаем их
COPY requirements.txt /app/
RUN python -m pip install --no-cache-dir -r /app/requirements.txt

# Копируем всё содержимое проекта в рабочую директорию
COPY . /app/
RUN echo "" > .env

# Применяем миграции Django
CMD ["python", "manage.py", "migrate"]

# Открываем порт 8000 для обращения к приложению
EXPOSE 8000

# Запускаем сервер Django
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
