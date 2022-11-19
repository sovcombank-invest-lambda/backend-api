# Команда lambda()

## **Sovcombank** Team Challenge 2022

## Оглавление

* Архитектура
* Запуск
  * Подготовка
  * Файл .env 
  * Алгоритм запуска
    * чета
    * чета
  * Проблемы с make
* Пример
* О команде

## Архитектура

https://excalidraw.com/#json=8HYGdFrSr4340yZNbFGko,VPAlxhpncFqpwd76Xy9VCA

## Запуск

### Подготовка

Для запуска нашего решение требуется наличие на рабочей машине следующих программ и утилит:
- Python v3.10
- Make v3.81
- Docker v20.10.21

### Файл .env

В решении используется `.env` файл, пример:

```
POSTGRES_DATABASE=invest 
POSTGRES_USERNAME=invest-user 
POSTGRES_PASSWORD=invest-user-password 
POSTGRES_HOST=92.63.102.99 
POSTGRES_PORT=5433 
 
FASTAPI_SECRET=some-secret-string 
FASTAPI_HASH_ALGORITHM=HS256 
FASTAPI_HASH_EXPIRATION=3600 
FASTAPI_PORT=8000
```

### Алгоритм запуска

#### Установка зависимостей

Установка происходит следующим образом:

```makefile
make prepare
```

#### Поднятие базы данных

Запуск Docker следущим образом:

```makefile
make services
```

#### Запуск сервиса

Когда все предыдущие шаги выполнены вы можете запустить решение

```makefile
make run
```

### Проблемы с make

Если у вас возникли проблемы с make, то шаги следующие:

```makefile
# Установка зависимостей
pip install -r requirements.txt

# Services
docker compose down
docker compose up -d postgresql

# Run
cd migrations && python -m alembic upgrade head
python -m uvicorn service.__main__:app  --host 0.0.0.0 --port=${FASTAPI_PORT} --log-level=warning --reload &
```

## Пример

Пример работающего решения можно увидеть по ссылке http://92.63.102.99:8000/docs

## О команде

* Егор **Смурыгин** - Менеджер
* Вячеслав **Лавров** - Frontend
* Татьяна **Лебедева** - Mobile
* Денис **Лахтионов **- Дизайнер
* Илья **Тампио** - ml-специалист

