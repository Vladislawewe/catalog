from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from sqlalchemy.sql import func
from sqlalchemy.orm import validates
import re
from datetime import datetime

db = SQLAlchemy()


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    reviews = db.relationship('Review', backref='user', lazy=True)

    @validates('first_name', 'last_name')
    def validate_names(self, key, value):
        if not value or len(value.strip()) < 1:
            raise ValueError(f"{key} не может быть пустым")
        if len(value) > 50:
            raise ValueError(f"{key} не может быть длиннее 50 символов")
        if not re.match(r'^[A-Za-zА-Яа-яЁё\s-]+$', value):
            raise ValueError(f"{key} содержит недопустимые символы")
        return value.strip()

    @validates('email')
    def validate_email(self, key, value):
        if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', value):
            raise ValueError("Некорректный формат email")
        if len(value) > 100:
            raise ValueError("Email не может быть длиннее 100 символов")
        return value.lower().strip()


class Genre(db.Model):
    __tablename__ = 'genres'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    parent_id = db.Column(db.Integer, db.ForeignKey('genres.id'), nullable=True)
    parent = db.relationship('Genre', remote_side=[id], backref='subgenres', lazy=True)
    movies = db.relationship('Movie', backref='movie_genre_ref', lazy=True)

    def __str__(self):
        return self.name

    @validates('name')
    def validate_name(self, key, value):
        if not value or len(value.strip()) < 1:
            raise ValueError("Название жанра не может быть пустым")
        if len(value) > 50:
            raise ValueError("Название жанра не может быть длиннее 50 символов")
        return value.strip()

    @validates('parent_id')
    def validate_parent_id(self, key, value):
        if value == self.id:
            raise ValueError("Жанр не может быть своим собственным родителем")
        return value

    def get_depth(self):
        """Возвращает уровень вложенности жанра."""
        depth = 0
        current = self
        while current.parent:
            depth += 1
            current = current.parent
        return depth

    def get_all_subgenres(self):
        """Рекурсивно собирает все поджанры."""
        result = []
        for subgenre in self.subgenres:
            result.append(subgenre)
            result.extend(subgenre.get_all_subgenres())
        return result


class Movie(db.Model):
    __tablename__ = 'movies'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    genre_id = db.Column(db.Integer, db.ForeignKey('genres.id'))
    director_id = db.Column(db.Integer, db.ForeignKey('directors.id'))
    duration = db.Column(db.Integer, default=0)
    rating = db.Column(db.Numeric(3, 1))
    image_path = db.Column(db.String(255), default='images/missing_image.jpg')
    genre = db.relationship('Genre', backref='movie_genres', lazy=True)
    director = db.relationship('Director', backref='movies', lazy=True)
    reviews = db.relationship('Review', backref='movie', lazy=True)
    actors = db.relationship('Actor', secondary='movie_actors', backref='movies', lazy=True)

    def update_rating(self):
        """Обновляет рейтинг фильма на основе среднего рейтинга отзывов."""
        avg_rating = db.session.query(func.avg(Review.rating)).filter(Review.movie_id == self.id).scalar()
        self.rating = round(float(avg_rating), 1) if avg_rating else None
        db.session.commit()

    @validates('title')
    def validate_title(self, key, value):
        if not value or len(value.strip()) < 1:
            raise ValueError("Название фильма не может быть пустым")
        if len(value) > 100:
            raise ValueError("Название фильма не может быть длиннее 100 символов")
        return value.strip()

    @validates('year')
    def validate_year(self, key, value):
        current_year = datetime.now().year
        if not (1888 <= value <= current_year):
            raise ValueError(f"Год должен быть между 1888 и {current_year}")
        return value

    @validates('duration')
    def validate_duration(self, key, value):
        if value < 0:
            raise ValueError("Длительность не может быть отрицательной")
        return value

    @validates('rating')
    def validate_rating(self, key, value):
        if value is not None and not (0 <= value <= 10):
            raise ValueError("Рейтинг должен быть между 0 и 10")
        return value

    @validates('image_path')
    def validate_image_path(self, key, value):
        if not value.startswith('images/'):
            raise ValueError("Путь к изображению должен начинаться с 'images/'")
        if len(value) > 255:
            raise ValueError("Путь к изображению не может быть длиннее 255 символов")
        return value


class Review(db.Model):
    __tablename__ = 'reviews'
    id = db.Column(db.Integer, primary_key=True)
    movie_id = db.Column(db.Integer, db.ForeignKey('movies.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    rating = db.Column(db.Numeric(3, 1), default=0, nullable=False)
    comment = db.Column(db.Text, default='')

    @validates('rating')
    def validate_rating(self, key, value):
        if not (0 <= value <= 10):
            raise ValueError("Рейтинг должен быть между 0 и 10")
        return value

    @validates('comment')
    def validate_comment(self, key, value):
        if len(value) > 1000:
            raise ValueError("Комментарий не может быть длиннее 1000 символов")
        return value


class Actor(db.Model):
    __tablename__ = 'actors'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)

    @validates('first_name', 'last_name')
    def validate_names(self, key, value):
        if not value or len(value.strip()) < 1:
            raise ValueError(f"{key} не может быть пустым")
        if len(value) > 50:
            raise ValueError(f"{key} не может быть длиннее 50 символов")
        if not re.match(r'^[A-Za-zА-Яа-яЁё\s-]+$', value):
            raise ValueError(f"{key} содержит недопустимые символы")
        return value.strip()


class MovieActor(db.Model):
    __tablename__ = 'movie_actors'
    id = db.Column(db.Integer, primary_key=True)
    movie_id = db.Column(db.Integer, db.ForeignKey('movies.id'), nullable=False)
    actor_id = db.Column(db.Integer, db.ForeignKey('actors.id'), nullable=False)

    __table_args__ = (
        db.UniqueConstraint('movie_id', 'actor_id', name='uq_movie_actor'),
    )


class Director(db.Model):
    __tablename__ = 'directors'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)

    @validates('first_name', 'last_name')
    def validate_names(self, key, value):
        if not value or len(value.strip()) < 1:
            raise ValueError(f"{key} не может быть пустым")
        if len(value) > 50:
            raise ValueError(f"{key} не может быть длиннее 50 символов")
        if not re.match(r'^[A-Za-zА-Яа-яЁё\s-]+$', value):
            raise ValueError(f"{key} содержит недопустимые символы")
        return value.strip()