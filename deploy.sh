#!/bin/bash

echo "Начинается развертывание приложения....."
docker compose down -v

docker system prune -f

docker compose build --no-cache
docker compose up -d
sleep 10

curl -f http://localhost:8000/docs

echo "Развертывание завершено успешно!"
