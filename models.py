from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from sqlalchemy.sql import func

db = SQLAlchemy()

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    reviews = db.relationship('Review', backref='user', lazy=True)

class Genre(db.Model):
    __tablename__ = 'genres'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    parent_id = db.Column(db.Integer, db.ForeignKey('genres.id'), nullable=True)
    parent = db.relationship('Genre', remote_side=[id], backref='subgenres', lazy=True)
    movies = db.relationship('Movie', backref='movie_genre_ref', lazy=True)

    def __str__(self):
        return self.name

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
    duration = db.Column(db.Integer)
    rating = db.Column(db.Numeric(3,1))
    image_path = db.Column(db.String(255))
    genre = db.relationship('Genre', backref='movie_genres', lazy=True)
    director = db.relationship('Director', backref='movies', lazy=True)
    reviews = db.relationship('Review', backref='movie', lazy=True)
    actors = db.relationship('Actor', secondary='movie_actors', backref='movies', lazy=True)

    def update_rating(self):
        """Обновляет рейтинг фильма на основе среднего рейтинга отзывов."""
        avg_rating = db.session.query(func.avg(Review.rating)).filter(Review.movie_id == self.id).scalar()
        self.rating = round(float(avg_rating), 1) if avg_rating else None
        db.session.commit()

class Review(db.Model):
    __tablename__ = 'reviews'
    id = db.Column(db.Integer, primary_key=True)
    movie_id = db.Column(db.Integer, db.ForeignKey('movies.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    rating = db.Column(db.Numeric(3,1))
    comment = db.Column(db.Text)

class Actor(db.Model):
    __tablename__ = 'actors'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)

class MovieActor(db.Model):
    __tablename__ = 'movie_actors'
    id = db.Column(db.Integer, primary_key=True)
    movie_id = db.Column(db.Integer, db.ForeignKey('movies.id'), nullable=False)
    actor_id = db.Column(db.Integer, db.ForeignKey('actors.id'), nullable=False)

class Director(db.Model):
    __tablename__ = 'directors'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)