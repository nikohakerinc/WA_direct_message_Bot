# Установка базового образа (host OS) из DockerHub
FROM python:3.10.11-alpine3.16

# Запускаем команду pip install для всех необходимых библиотек
RUN pip install --upgrade pip \
&& pip install python-dotenv \
&& pip install aiogram

# Создаем директорию
WORKDIR /opt/tg_bot/

# Копируем в папку /opt/tg_bot файл bot.py
COPY bot.py /opt/tg_bot/

# Указываем переменную окружения TOKEN
ENV TOKEN=<YOUR_TELEGRAM_BOT_TOKEN>

# Запускаем bot.py
CMD ["python", "bot.py"]