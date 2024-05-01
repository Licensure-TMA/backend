#!/bin/bash

# Путь к скрипту deploy.sh
DEPLOY_SCRIPT=/home/defendershow/backend/deploy/deploy.sh

# Отправить заголовки HTTP
echo -e "HTTP/1.1 200 OK\nContent-Type: text/plain\n"

# Запустить скрипт развертывания
$DEPLOY_SCRIPT

# Вернуть ответ веб-хуку
echo "Deployment triggered successfully."