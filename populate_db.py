from app import app, db
from models import User, Movie, Genre, Director, Actor, Review
from werkzeug.security import generate_password_hash

with app.app_context():
    def remove_duplicate_movies():
        duplicates = (
            db.session.query(Movie.title, Movie.year)
            .group_by(Movie.title, Movie.year)
            .having(db.func.count() > 1)
            .all()
        )
        for title, year in duplicates:
            movies = Movie.query.filter_by(title=title, year=year).order_by(Movie.id).all()
            for movie in movies[1:]:
                Review.query.filter_by(movie_id=movie.id).delete()
                db.session.execute(db.text("DELETE FROM movie_actors WHERE movie_id = :movie_id"), {"movie_id": movie.id})
                db.session.delete(movie)
        db.session.commit()

    remove_duplicate_movies()

    # Создание иерархии жанров
    genres = {}
    genre_data = [
        ('Боевик', None),
        ('Военный боевик', 'Боевик'),
        ('Приключенческий боевик', 'Боевик'),
        ('Драма', None),
        ('Историческая драма', 'Драма'),
        ('Мелодрама', 'Драма'),
        ('Комедия', None),
        ('Фантастика', None),
        ('Триллер', None)
    ]
    for name, parent_name in genre_data:
        genre = Genre.query.filter_by(name=name).first()
        if not genre:
            genre = Genre(name=name)
            if parent_name:
                parent = Genre.query.filter_by(name=parent_name).first()
                if parent:
                    genre.parent_id = parent.id
            db.session.add(genre)
        genres[name] = genre
    db.session.commit()

    # Проверяем и создаем режиссеров
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

    # Проверяем и создаем актеров
    actors_data = [
        ('Том', 'Хэнкс'), ('Леонардо', 'ДиКаприо'), ('Брюс', 'Уиллис'),
        ('Брэд', 'Питт'), ('Анджелина', 'Джоли'), ('Роберт', 'Де Ниро'),
        ('Скарлетт', 'Йоханссон'), ('Морган', 'Фримен'), ('Кейт', 'Уинслет'),
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

    # Проверяем и создаем пользователей
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

    # Создание исходных фильмов с поджанрами
    movie1 = Movie(
        title='Спасти рядового Райана',
        year=1998,
        genre=genres['Военный боевик'],
        director=directors['Стивен Спилберг'],
        duration=169,
        image_path='images/saving_private_ryan.jpg'
    )
    movie1.actors.append(actors['Том Хэнкс'])

    movie2 = Movie(
        title='Начало',
        year=2010,
        genre=genres['Приключенческий боевик'],
        director=directors['Кристофер Нолан'],
        duration=148,
        image_path='images/inception.jpg'
    )
    movie2.actors.append(actors['Леонардо ДиКаприо'])

    movie3 = Movie(
        title='Темный рыцарь',
        year=2008,
        genre=genres['Приключенческий боевик'],
        director=directors['Кристофер Нолан'],
        duration=152,
        image_path='images/the_dark_knight.jpg'
    )
    movie3.actors.append(actors['Киллиан Мёрфи'])

    # Проверка и добавление исходных фильмов
    for movie in [movie1, movie2, movie3]:
        if not Movie.query.filter_by(title=movie.title, year=movie.year).first():
            db.session.add(movie)
    db.session.commit()

    # Добавление новых фильмов с поджанрами
    new_movies_data = [
        {
            'title': 'Бешеные псы',
            'year': 1992,
            'genre': genres['Приключенческий боевик'],
            'director': directors['Квентин Тарантино'],
            'duration': 99,
            'image_path': 'images/reservoir_dogs.jpg',
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
            'genre': genres['Мелодрама'],
            'director': directors['Джеймс Кэмерон'],
            'duration': 194,
            'image_path': 'images/titanic.jpg',
            'actors': [actors['Леонардо ДиКаприо'], actors['Кейт Уинслет']],
            'reviews': [
                {'user': users['alexey@example.com'], 'rating': 8.5, 'comment': 'Эмоциональная классика!'},
                {'user': users['ekaterina@example.com'], 'rating': 6.5, 'comment': 'Слишком мелодраматично.'},
                {'user': users['dmitry@example.com'], 'rating': 8.0, 'comment': 'Хорошая история.'}
            ]
        },
        {
            'title': 'Бойцовский клуб',
            'year': 1999,
            'genre': genres['Триллер'],
            'director': directors['Дэвид Финчер'],
            'duration': 139,
            'image_path': 'images/fight_club.jpg',
            'actors': [actors['Брэд Питт'], actors['Морган Фримен']],
            'reviews': [
                {'user': users['alexey@example.com'], 'rating': 9.5, 'comment': 'Шедевр!'},
                {'user': users['ekaterina@example.com'], 'rating': 7.0, 'comment': 'Сильный, но путающий.'},
                {'user': users['dmitry@example.com'], 'rating': 5.5, 'comment': 'Слишком странно.'}
            ]
        },
        {
            'title': 'Чужой',
            'year': 1979,
            'genre': genres['Фантастика'],
            'director': directors['Ридли Скотт'],
            'duration': 117,
            'image_path': 'images/alien.jpg',
            'actors': [actors['Скарлетт Йоханссон'], actors['Джонни Депп']],
            'reviews': [
                {'user': users['alexey@example.com'], 'rating': 8.0, 'comment': 'Классика!'},
                {'user': users['ekaterina@example.com'], 'rating': 6.0, 'comment': 'Страшно.'},
                {'user': users['dmitry@example.com'], 'rating': 7.5, 'comment': 'Атмосферно.'}
            ]
        },
        {
            'title': 'Таксист',
            'year': 1976,
            'genre': genres['Историческая драма'],
            'director': directors['Мартин Скорсезе'],
            'duration': 114,
            'image_path': 'images/taxi_driver.jpg',
            'actors': [actors['Роберт Де Ниро'], actors['Энн Хэтэуэй']],
            'reviews': [
                {'user': users['alexey@example.com'], 'rating': 8.5, 'comment': 'Глубокий фильм.'},
                {'user': users['ekaterina@example.com'], 'rating': 7.0, 'comment': 'Тяжелый.'},
                {'user': users['dmitry@example.com'], 'rating': 6.5, 'comment': 'Не всем зайдет.'}
            ]
        },
        {
            'title': 'Рок-н-рольщик',
            'year': 2008,
            'genre': genres['Приключенческий боевик'],
            'director': directors['Гай Ричи'],
            'duration': 114,
            'image_path': 'images/rocknrolla.jpg',
            'actors': [actors['Том Харди'], actors['Эмили Блант']],
            'reviews': [
                {'user': users['alexey@example.com'], 'rating': 7.5, 'comment': 'Динамично!'},
                {'user': users['ekaterina@example.com'], 'rating': 6.5, 'comment': 'Запутанный.'},
                {'user': users['dmitry@example.com'], 'rating': 8.0, 'comment': 'Крутой стиль!'}
            ]
        },
        {
            'title': 'Любовное настроение',
            'year': 2000,
            'genre': genres['Мелодрама'],
            'director': directors['Вонг Кар-вай'],
            'duration': 98,
            'image_path': 'images/in_the_mood_for_love.jpg',
            'actors': [actors['Райан Гослинг'], actors['Эмма Стоун']],
            'reviews': [
                {'user': users['alexey@example.com'], 'rating': 8.5, 'comment': 'Красиво!'},
                {'user': users['ekaterina@example.com'], 'rating': 7.0, 'comment': 'Атмосферно.'},
                {'user': users['dmitry@example.com'], 'rating': 6.0, 'comment': 'Скучновато.'}
            ]
        },
        {
            'title': 'Дюна',
            'year': 2021,
            'genre': genres['Фантастика'],
            'director': directors['Дени Вильнёв'],
            'duration': 155,
            'image_path': 'images/dune.jpg',
            'actors': [actors['Зендая Абобовна'], actors['Тимоти Шаламе']],
            'reviews': [
                {'user': users['alexey@example.com'], 'rating': 9.0, 'comment': 'Эпично!'},
                {'user': users['ekaterina@example.com'], 'rating': 7.5, 'comment': 'Затянуто.'},
                {'user': users['dmitry@example.com'], 'rating': 6.5, 'comment': 'Не понял.'}
            ]
        },
        {
            'title': 'Паразиты',
            'year': 2019,
            'genre': genres['Триллер'],
            'director': directors['Бонг Джун-хо'],
            'duration': 132,
            'image_path': 'images/parasite.jpg',
            'actors': [actors['Сон Кан-хо'], actors['Чхве Мин-сик']],
            'reviews': [
                {'user': users['alexey@example.com'], 'rating': 9.5, 'comment': 'Гениально!'},
                {'user': users['ekaterina@example.com'], 'rating': 8.0, 'comment': 'Мрачно.'},
                {'user': users['dmitry@example.com'], 'rating': 7.0, 'comment': 'Переоценен.'}
            ]
        },
        {
            'title': 'Доктор Стрэндж',
            'year': 2016,
            'genre': genres['Фантастика'],
            'director': directors['Скотт Дерриксон'],
            'duration': 115,
            'image_path': 'images/doctor_strange.jpg',
            'actors': [actors['Бенедикт Камбербэтч'], actors['Тильда Свинтон']],
            'reviews': [
                {'user': users['alexey@example.com'], 'rating': 8.0, 'comment': 'Зрелищно!'},
                {'user': users['ekaterina@example.com'], 'rating': 6.7, 'comment': 'Предсказуемо.'},
                {'user': users['dmitry@example.com'], 'rating': 7.5, 'comment': 'Не шедевр.'}
            ]
        }
    ]

    # Добавление новых фильмов
    for movie_data in new_movies_data:
        if not Movie.query.filter_by(title=movie_data['title'], year=movie_data['year']).first():
            movie = Movie(
                title=movie_data['title'],
                year=movie_data['year'],
                genre=movie_data['genre'],
                director=movie_data['director'],
                duration=movie_data['duration'],
                image_path=movie_data['image_path']
            )
            for actor in movie_data['actors']:
                movie.actors.append(actor)
            db.session.add(movie)
            db.session.commit()
            for review_data in movie_data['reviews']:
                review = Review(
                    movie=movie,
                    user=review_data['user'],
                    rating=review_data.get('rating', 0),
                    comment=review_data.get('comment', '')
                )
                db.session.add(review)
            db.session.commit()
            movie.update_rating()

    # Добавление отзывов для исходных фильмов
    existing_reviews = [
        {'movie': movie1, 'user': users['ivan@example.com'], 'rating': 9.0, 'comment': 'Отличный фильм!'},
        {'movie': movie1, 'user': users['ekaterina@example.com'], 'rating': 7.5, 'comment': 'Слишком длинный.'},
        {'movie': movie1, 'user': users['dmitry@example.com'], 'rating': 6.5, 'comment': 'Не зацепило.'},
        {'movie': movie2, 'user': users['maria@example.com'], 'rating': 8.5, 'comment': 'Умопомрачительный!'},
        {'movie': movie2, 'user': users['alexey@example.com'], 'rating': 9.0, 'comment': 'Крутой фильм!'},
        {'movie': movie2, 'user': users['dmitry@example.com'], 'rating': 6.0, 'comment': 'Сложно следить.'},
        {'movie': movie3, 'user': users['alexey@example.com'], 'rating': 9.5, 'comment': 'Лучший Нолан!'},
        {'movie': movie3, 'user': users['ekaterina@example.com'], 'rating': 7.0, 'comment': 'Переоценен.'},
        {'movie': movie3, 'user': users['dmitry@example.com'], 'rating': 6.6, 'comment': 'Запутанный.'}
    ]
    for review_data in existing_reviews:
        if not Review.query.filter_by(movie_id=review_data['movie'].id, user_id=review_data['user'].id, comment=review_data['comment']).first():
            review = Review(
                movie=review_data['movie'],
                user=review_data['user'],
                rating=review_data.get('rating', 0),
                comment=review_data.get('comment', '')
            )
            db.session.add(review)
    db.session.commit()

    for movie in [movie1, movie2, movie3]:
        movie.update_rating()

print("База данных успешно заполнена!")