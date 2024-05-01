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

# Даем права на исполнение скрипту start_gunicorn.sh
RUN chmod +x start_gunicorn.sh

# Открываем порт 8082
EXPOSE 8082

# Запускаем скрипт start_gunicorn.sh при старте контейнера
CMD ["./start_gunicorn.sh"]
