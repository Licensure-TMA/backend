#!/bin/bash

# Остановить и удалить старый контейнер, если он существует
docker stop back || true
docker rm back || true

# Удалить старый образ
docker rmi aleksglebov/licensure:back || true

# Получить последнюю версию образа из Docker Hub
docker pull aleksglebov/licensure:back

# Запустить новый контейнер
docker run -p 8082:8082 -d --name back aleksglebov/licensure:back

echo "Deployment completed successfully."