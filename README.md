# Каталог фильмов — Flask + PostgreSQL

## Описание
Веб-приложение для ведения каталога фильмов с поддержкой отзывов, актёров, режиссёров и пользователей.

## Запуск проекта

1. Клонируйте репозиторий.
2. Создайте и активируйте виртуальное окружение.
3. Установите зависимости:
   ```
   pip install -r requirements.txt
   ```
4. Настройте переменные окружения и подключение к PostgreSQL (см. `config.py`).
5. Инициализируйте базу данных:
   ```
   flask db init
   flask db migrate
   flask db upgrade
   ```
6. Запустите сервер:
   ```
   python run.py
   ```

## Структура таблиц

- **Movies** (`id`, `title`, `year`, `genre_id`, `duration`, `rating`, `director_id`)
- **Directors** (`id`, `first_name`, `last_name`)
- **Actors** (`id`, `first_name`, `last_name`)
- **MovieActors** (`id`, `movie_id`, `actor_id`)
- **Genres** (`id`, `name`)
- **Users** (`id`, `first_name`, `last_name`, `email`)
- **Reviews** (`id`, `movie_id`, `user_id`, `rating`, `comment`)

## ER-диаграмма

ER-диаграмма находится в файле `ER_diagram.png`.

### Вербальные фразы и роли

- MovieActors связывает Movies и Actors. Роли: "фильм", "актёр".
- Reviews связывает Users и Movies. Роли: "пользователь", "фильм".
- Genre — жанр фильма.
- Director — режиссёр фильма.

## Примечания

- Все связи реализованы через внешние ключи и поддерживают целостность (ON DELETE CASCADE).
- Email пользователя уникален.
- Оценка фильмов и отзывов — от 0 до 10.
- Представление TopRatedMovies — топ-10 фильмов по рейтингу.

## Лицензия

MIT