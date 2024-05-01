#!/bin/bash

# Генерируем случайный секретный ключ
SECRET_KEY=$(openssl rand -base64 32)

# Добавляем секретный ключ в файл /etc/environment
echo "SECRET_KEY='$SECRET_KEY'" | sudo tee -a /etc/environment