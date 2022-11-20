# Команда lambda()

## **Sovcombank** Team Challenge 2022

## Оглавление

* Архитектура
* Фичи
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

Бэкэнд построен с использованием архитектурного паттерна MVC, где роль `model` - выполняют модели БД из модуля  `migrations/models`,
`View` - это `pydantic` модели из модуля service/schematic,
`Controller` - это ручки из модуля service/endpoints 
это в купе с используемым на всем проекте  паттерне Стратегия (выполненом путем разделения кода по модулям в древовидной структуре проекта) позволяет легко поддерживать код, и масштабировать его, добавляя новые фичи

Для реализацции системы асинхронных промизов для осущестления подтверждения регистрации, создания очереди на получения исторической сводки о транзакциях используется паттерн State

При проверки прав пользователей используется паттерн `Chain of Responsibility`

При создании истории транзакций использовуется паттерн `Memento`

В итоге код разделен на изолированные участки кода, код достаточно легко масштабируется, и легко поддерживается, используются понятные структуры.

## Фичи

Ролевая модель: `service/models/users.py`

Регистрация: `service/endpoints/auth.py`

Подтверждение регистрации/ блокировка пользователей: `service/endpoints/admin.py`

Создание / Ведение брокерского счета / Функционал валютного счета: `service/endpoits/currency_account.py`

Отображение сводки транзакциях по валютному счету: `service/endpoints/statistics.py`

Историческая информация движения валюты: `service/endpoints/exchange_rates.py`

Функционал торговли (Добавление / Перевод валюты между валютными счетами согласно курсу):

* `service/utils/currency.py`
* `service/services/currency_account.py`

Визуализация графиков: https://github.com/sovcombank-invest-lambda/charts
Прогноз валюты: 

* https://github.com/sovcombank-invest-lambda/stock-price-prediction
* `service/utils/predict.py` - код предсказаний

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

## PS

Для тестирование админских функций уже существует пользователь с

* username: a
* password: a
