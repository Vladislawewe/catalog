from app import app, db
from models import User, Movie, Genre, Director, Actor, Review
from werkzeug.security import generate_password_hash

# Используем контекст приложения Flask для работы с базой данных
with app.app_context():
    # Проверяем и создаем жанры, если их еще нет
    genres = {name: Genre.query.filter_by(name=name).first() or Genre(name=name)
              for name in ['Боевик', 'Комедия', 'Драма', 'Фантастика', 'Триллер']}
    for genre in genres.values():
        if genre not in db.session:
            db.session.add(genre)
    db.session.commit()

    # Проверяем и создаем режиссеров, если их еще нет
    directors_data = [
        ('Стивен', 'Спилберг'), ('Кристофер', 'Нолан'),
        ('Квентин', 'Тарантино'), ('Джеймс', 'Кэмерон'), ('Дэвид', 'Финчер'),
        ('Ридли', 'Скотт'), ('Мартин', 'Скорсезе'), ('Гай', 'Ричи'),
        ('Вонг', 'Кар-вай'), ('Дени', 'Вильнёв'), ('Бонг', 'Джун-хо'),
        ('Скотт', 'Дерриксон')
    ]
    directors = {}
    for fname, lname in directors_data:
        director = Director.query.filter_by(first_name=fname, last_name=lname).first()
        if not director:
            director = Director(first_name=fname, last_name=lname)
            db.session.add(director)
        directors[f"{fname} {lname}"] = director
    db.session.commit()

    # Проверяем и создаем актеров, если их еще нет
    actors_data = [
        ('Том', 'Хэнкс'), ('Леонардо', 'ДиКаприо'), ('Брюс', 'Уиллис'),
        ('Брэд', 'Питт'), ('Анджелина', 'Джоли'), ('Роберт', 'Де Ниро'),
        ('Скарлетт', 'Йоханссон'), ('Морган', 'Фриман'), ('Кейт', 'Уинслет'),
        ('Джонни', 'Депп'), ('Энн', 'Хэтэуэй'), ('Хоакин', 'Феникс'),
        ('Зендая', 'Абобовна'), ('Том', 'Харди'), ('Эмили', 'Блант'),
        ('Райан', 'Гослинг'), ('Эмма', 'Стоун'), ('Киллиан', 'Мёрфи'),
        ('Сон', 'Кан-хо'), ('Чхве', 'Мин-сик'), ('Тильда', 'Свинтон'),
        ('Бенедикт', 'Камбербэтч'), ('Тимоти', 'Шаламе')
    ]
    actors = {}
    for fname, lname in actors_data:
        actor = Actor.query.filter_by(first_name=fname, last_name=lname).first()
        if not actor:
            actor = Actor(first_name=fname, last_name=lname)
            db.session.add(actor)
        actors[f"{fname} {lname}"] = actor
    db.session.commit()

    # Проверяем и создаем пользователей, если их еще нет
    users_data = [
        ('Иван', 'Иванов', 'ivan@example.com', 'password'),
        ('Мария', 'Петрова', 'maria@example.com', 'password'),
        ('Алексей', 'Смирнов', 'alexey@example.com', 'password'),
        ('Екатерина', 'Кузнецова', 'ekaterina@example.com', 'password'),
        ('Дмитрий', 'Попов', 'dmitry@example.com', 'password')
    ]
    users = {}
    for fname, lname, email, pwd in users_data:
        user = User.query.filter_by(email=email).first()
        if not user:
            user = User(
                first_name=fname,
                last_name=lname,
                email=email,
                password=generate_password_hash(pwd)
            )
            db.session.add(user)
        users[email] = user
    db.session.commit()

    # Создание исходных фильмов
    movie1 = Movie(
        title='Спасти рядового Райана',
        year=1998,
        genre=genres['Боевик'],
        director=directors['Стивен Спилберг'],
        duration=169
    )
    movie1.actors.append(actors['Том Хэнкс'])

    movie2 = Movie(
        title='Начало',
        year=2010,
        genre=genres['Боевик'],
        director=directors['Кристофер Нолан'],
        duration=148
    )
    movie2.actors.append(actors['Леонардо ДиКаприо'])

    movie3 = Movie(
        title='Темный рыцарь',
        year=2008,
        genre=genres['Боевик'],
        director=directors['Кристофер Нолан'],
        duration=152
    )
    movie3.actors.append(actors['Киллиан Мёрфи'])

    # Добавление 10 новых фильмов
    new_movies_data = [
        {
            'title': 'Бешеные псы',
            'year': 1992,
            'genre': genres['Боевик'],
            'director': directors['Квентин Тарантино'],
            'duration': 99,
            'actors': [actors['Брэд Питт'], actors['Хоакин Феникс']],
            'reviews': [
                {'user': users['alexey@example.com'], 'rating': 9.0, 'comment': 'Культовый фильм, отличная режиссура!'},
                {'user': users['ekaterina@example.com'], 'rating': 7.5, 'comment': 'Хороший, но слишком много насилия.'},
                {'user': users['dmitry@example.com'], 'rating': 6.0, 'comment': 'Сюжет интересный, но затянуто.'}
            ]
        },
        {
            'title': 'Титаник',
            'year': 1997,
            'genre': genres['Драма'],
            'director': directors['Джеймс Кэмерон'],
            'duration': 194,
            'actors': [actors['Леонардо ДиКаприо'], actors['Кейт Уинслет']],
            'reviews': [
                {'user': users['alexey@example.com'], 'rating': 8.5, 'comment': 'Эмоциональная классика, до слез!'},
                {'user': users['ekaterina@example.com'], 'rating': 6.5, 'comment': 'Слишком мелодраматично для меня.'},
                {'user': users['dmitry@example.com'], 'rating': 8.0, 'comment': 'Хорошая история, отличные актеры.'}
            ]
        },
        {
            'title': 'Бойцовский клуб',
            'year': 1999,
            'genre': genres['Триллер'],
            'director': directors['Дэвид Финчер'],
            'duration': 139,
            'actors': [actors['Брэд Питт'], actors['Морган Фриман']],
            'reviews': [
                {'user': users['alexey@example.com'], 'rating': 9.5, 'comment': 'Шедевр, неожиданный поворот!'},
                {'user': users['ekaterina@example.com'], 'rating': 7.0, 'comment': 'Сильный, но путающий.'},
                {'user': users['dmitry@example.com'], 'rating': 5.5, 'comment': 'Не понял смысла, слишком странно.'}
            ]
        },
        {
            'title': 'Чужой',
            'year': 1979,
            'genre': genres['Фантастика'],
            'director': directors['Ридли Скотт'],
            'duration': 117,
            'actors': [actors['Скарлетт Йоханссон'], actors['Джонни Депп']],
            'reviews': [
                {'user': users['alexey@example.com'], 'rating': 8.0, 'comment': 'Классика научной фантастики!'},
                {'user': users['ekaterina@example.com'], 'rating': 6.0, 'comment': 'Страшно, но не мое.'},
                {'user': users['dmitry@example.com'], 'rating': 7.5, 'comment': 'Атмосферный, но староват.'}
            ]
        },
        {
            'title': 'Таксист',
            'year': 1976,
            'genre': genres['Драма'],
            'director': directors['Мартин Скорсезе'],
            'duration': 114,
            'actors': [actors['Роберт Де Ниро'], actors['Энн Хэтэуэй']],
            'reviews': [
                {'user': users['alexey@example.com'], 'rating': 8.5, 'comment': 'Глубокий и мрачный фильм.'},
                {'user': users['ekaterina@example.com'], 'rating': 7.0, 'comment': 'Хороший, но тяжелый.'},
                {'user': users['dmitry@example.com'], 'rating': 6.5, 'comment': 'Не всем зайдет.'}
            ]
        },
        {
            'title': 'Рок-н-рольщик',
            'year': 2008,
            'genre': genres['Боевик'],
            'director': directors['Гай Ричи'],
            'duration': 114,
            'actors': [actors['Том Харди'], actors['Эмили Блант']],
            'reviews': [
                {'user': users['alexey@example.com'], 'rating': 7.5, 'comment': 'Динамично и стильно!'},
                {'user': users['ekaterina@example.com'], 'rating': 6.5, 'comment': 'Слишком запутанный сюжет.'},
                {'user': users['dmitry@example.com'], 'rating': 8.0, 'comment': 'Крутой стиль Ричи!'}
            ]
        },
        {
            'title': 'Любовное настроение',
            'year': 2000,
            'genre': genres['Драма'],
            'director': directors['Вонг Кар-вай'],
            'duration': 98,
            'actors': [actors['Райан Гослинг'], actors['Эмма Стоун']],
            'reviews': [
                {'user': users['alexey@example.com'], 'rating': 8.5, 'comment': 'Красивая и эмоциональная история.'},
                {'user': users['ekaterina@example.com'], 'rating': 7.0, 'comment': 'Медленный, но атмосферный.'},
                {'user': users['dmitry@example.com'], 'rating': 6.0, 'comment': 'Скучновато, не зацепило.'}
            ]
        },
        {
            'title': 'Дюна',
            'year': 2021,
            'genre': genres['Фантастика'],
            'director': directors['Дени Вильнёв'],
            'duration': 155,
            'actors': [actors['Зендая Абобовна'], actors['Тимоти Шаламе']],
            'reviews': [
                {'user': users['alexey@example.com'], 'rating': 9.0, 'comment': 'Эпичная экранизация!'},
                {'user': users['ekaterina@example.com'], 'rating': 7.5, 'comment': 'Красиво, но затянуто.'},
                {'user': users['dmitry@example.com'], 'rating': 6.5, 'comment': 'Не понял всей шумихи.'}
            ]
        },
        {
            'title': 'Паразиты',
            'year': 2019,
            'genre': genres['Триллер'],
            'director': directors['Бонг Джун-хо'],
            'duration': 132,
            'actors': [actors['Сон Кан-хо'], actors['Чхве Мин-сик']],
            'reviews': [
                {'user': users['alexey@example.com'], 'rating': 9.5, 'comment': 'Гениальный фильм!'},
                {'user': users['ekaterina@example.com'], 'rating': 8.0, 'comment': 'Интересно, но мрачно.'},
                {'user': users['dmitry@example.com'], 'rating': 7.0, 'comment': 'Хороший, но переоцененный.'}
            ]
        },
        {
            'title': 'Доктор Стрэндж',
            'year': 2016,
            'genre': genres['Фантастика'],
            'director': directors['Скотт Дерриксон'],
            'duration': 115,
            'actors': [actors['Бенедикт Камбербэтч'], actors['Тильда Свинтон']],
            'reviews': [
                {'user': users['alexey@example.com'], 'rating': 8.0, 'comment': 'Классные визуальные эффекты!'},
                {'user': users['ekaterina@example.com'], 'rating': 6.5, 'comment': 'Сюжет предсказуемый.'},
                {'user': users['dmitry@example.com'], 'rating': 7.5, 'comment': 'Зрелищно, но не шедевр.'}
            ]
        }
    ]

    # Проверка и добавление исходных фильмов
    for movie in [movie1, movie2, movie3]:
        if not Movie.query.filter_by(title=movie.title, year=movie.year).first():
            db.session.add(movie)
    db.session.commit()

    # Добавление новых фильмов
    for movie_data in new_movies_data:
        existing_movie = Movie.query.filter_by(title=movie_data['title'], year=movie_data['year']).first()
        if not existing_movie:
            movie = Movie(
                title=movie_data['title'],
                year=movie_data['year'],
                genre=movie_data['genre'],
                director=movie_data['director'],
                duration=movie_data['duration']
            )
            for actor in movie_data['actors']:
                movie.actors.append(actor)
            db.session.add(movie)
            db.session.commit()  # Коммитим фильм для получения ID

            # Добавляем отзывы
            for review_data in movie_data['reviews']:
                review = Review(
                    movie=movie,
                    user=review_data['user'],
                    rating=review_data['rating'],
                    comment=review_data['comment']
                )
                db.session.add(review)
            db.session.commit()
            movie.update_rating()  # Обновляем рейтинг фильма

    # Добавление отзывов для исходных фильмов
    existing_reviews = [
        {'movie': movie1, 'user': users['ivan@example.com'], 'rating': 9.0, 'comment': 'Отличный фильм!'},
        {'movie': movie1, 'user': users['ekaterina@example.com'], 'rating': 7.5, 'comment': 'Хороший, но слишком длинный.'},
        {'movie': movie1, 'user': users['dmitry@example.com'], 'rating': 6.5, 'comment': 'Не зацепило.'},
        {'movie': movie2, 'user': users['maria@example.com'], 'rating': 8.5, 'comment': 'Умопомрачительный сюжет!'},
        {'movie': movie2, 'user': users['alexey@example.com'], 'rating': 9.0, 'comment': 'Крутой фильм!'},
        {'movie': movie2, 'user': users['dmitry@example.com'], 'rating': 6.0, 'comment': 'Сложно следить за сюжетом.'},
        {'movie': movie3, 'user': users['alexey@example.com'], 'rating': 9.5, 'comment': 'Лучший фильм Нолана!'},
        {'movie': movie3, 'user': users['ekaterina@example.com'], 'rating': 7.0, 'comment': 'Хорош, но переоценен.'},
        {'movie': movie3, 'user': users['dmitry@example.com'], 'rating': 6.5, 'comment': 'Сюжет запутанный.'}
    ]
    for review_data in existing_reviews:
        if not Review.query.filter_by(movie_id=review_data['movie'].id, user_id=review_data['user'].id, comment=review_data['comment']).first():
            review = Review(
                movie=review_data['movie'],
                user=review_data['user'],
                rating=review_data['rating'],
                comment=review_data['comment']
            )
            db.session.add(review)
    db.session.commit()

    # Обновляем рейтинги для исходных фильмов
    for movie in [movie1, movie2, movie3]:
        movie.update_rating()

print("База данных успешно заполнена!")