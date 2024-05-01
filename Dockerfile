# Используем официальный образ Python 3.9 в качестве базового
FROM python:3.9-slim

# Устанавливаем Gunicorn
RUN apt-get update && apt-get install -y gunicorn

# Устанавливаем рабочую директорию внутри контейнера
WORKDIR /app

# Копируем файл requirements.txt в рабочую директорию
COPY requirements.txt .

# Устанавливаем зависимости Python из requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Копируем остальные файлы в рабочую директорию
COPY . .

# Копируем SSL-сертификат и ключ с сервера в контейнер
COPY fullchain.pem /etc/letsencrypt/live/licensure.tech/
COPY privkey.pem /etc/letsencrypt/live/licensure.tech/

# Устанавливаем переменную окружения SECRET_KEY
ENV SECRET_KEY=$(cat environment | grep SECRET_KEY | cut -d '=' -f 2 | tr -d "'")

# Даем права на исполнение скрипту start_gunicorn.sh
RUN chmod +x start_gunicorn.sh

# Открываем порт 8082
EXPOSE 8082

# Запускаем скрипт start_gunicorn.sh при старте контейнера
CMD ["./start_gunicorn.sh"]