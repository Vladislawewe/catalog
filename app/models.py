from . import db

class Genre(db.Model):
    __tablename__ = 'genres'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)

class Director(db.Model):
    __tablename__ = 'directors'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))

class Actor(db.Model):
    __tablename__ = 'actors'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))

class Movie(db.Model):
    __tablename__ = 'movies'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    genre_id = db.Column(db.Integer, db.ForeignKey('genres.id'))
    duration = db.Column(db.Integer)
    rating = db.Column(db.Float)
    director_id = db.Column(db.Integer, db.ForeignKey('directors.id'))

    genre = db.relationship('Genre', backref='movies')
    director = db.relationship('Director', backref='movies')
    actors = db.relationship('MovieActor', back_populates='movie')
    reviews = db.relationship('Review', back_populates='movie')

class MovieActor(db.Model):
    __tablename__ = 'movie_actors'
    id = db.Column(db.Integer, primary_key=True)
    movie_id = db.Column(db.Integer, db.ForeignKey('movies.id', ondelete="CASCADE"))
    actor_id = db.Column(db.Integer, db.ForeignKey('actors.id', ondelete="CASCADE"))

    movie = db.relationship('Movie', back_populates='actors')
    actor = db.relationship('Actor', backref='movie_actors')

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    email = db.Column(db.String(120), unique=True, nullable=False)

    reviews = db.relationship('Review', back_populates='user')

class Review(db.Model):
    __tablename__ = 'reviews'
    id = db.Column(db.Integer, primary_key=True)
    movie_id = db.Column(db.Integer, db.ForeignKey('movies.id', ondelete="CASCADE"))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete="CASCADE"))
    rating = db.Column(db.Float, nullable=False)
    comment = db.Column(db.Text)

    movie = db.relationship('Movie', back_populates='reviews')
    user = db.relationship('User', back_populates='reviews')