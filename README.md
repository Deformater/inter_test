## Развёртывание
  создайте .env файл по образцу .env.example,
  далее используя docker compose:
  
    docker compose up -d --build
  
  после этого API будет поднята на 8000 порте(порт можно изменит в docker-compose.yml)

## P. S.
Также API уже поднята на https://api.weather.grimur.ru/

Документация OpenAPI3.0: https://api.weather.grimur.ru/docs
