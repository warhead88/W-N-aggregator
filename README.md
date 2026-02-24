# TeleNetAggregator (W-N-aggregator)
Telegram-бот на базе `aiogram 3.x`, агрегирующий новости с GNews API и погоду через OpenWeatherMap API, с функционалом ежедневной рассылки.

## Особенности
* Получение новостей по ключевым словам.
* Погода и прогноз на 3 дня.
* Ежедневная автоматическая рассылка погоды и новостей по расписанию, с учетом часового пояса пользователя.
* Postgres SQL как база данных (через SQLAlchemy 2.0+).
* Использование Docker и Docker Compose для удобного деплоя.

## Требования
* Docker
* Docker Compose

## Установка и запуск
1. Клонируйте проект:
   ```bash
   git clone <URL вашего репозитория> W-N-aggregator
   cd W-N-aggregator
   ```
2. Создайте файл `.env` на основе шаблона и заполните своими API ключами:
   ```bash
   cp .env.example .env
   ```
   > В `.env` вам нужно указать токены для `BOT_TOKEN` (от BotFather), `NEWS_API` (с gnews.io) и `WEATHER_API` (с openweathermap.org).

3. Запустите проект в Docker:
   ```bash
   docker-compose up -d --build
   ```

4. Остановка:
   ```bash
   docker-compose down
   ```

## Разработка
Для запуска локально (без Docker):
1. Склонируйте репозиторий.
2. Поднимите PostgreSQL на localhost или любой другой удобный сервер.
3. Установите зависимости: `pip install -r requirements.txt`.
4. Заполните `.env` переменными.
5. Запустите: `python bot.py`
