CREATE TABLE genres (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) UNIQUE NOT NULL
);

CREATE TABLE directors (
    id SERIAL PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL
);

CREATE TABLE actors (
    id SERIAL PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL
);

CREATE TABLE movies (
    id SERIAL PRIMARY KEY,
    title VARCHAR(100) NOT NULL,
    year INTEGER NOT NULL CHECK (year >= 1900),
    genre_id INTEGER REFERENCES genres(id) ON DELETE SET NULL,
    director_id INTEGER REFERENCES directors(id) ON DELETE SET NULL,
    duration INTEGER,
    rating NUMERIC(3,1) CHECK (rating >= 0 AND rating <= 10)
);

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(100) NOT NULL
);

CREATE TABLE reviews (
    id SERIAL PRIMARY KEY,
    movie_id INTEGER REFERENCES movies(id) ON DELETE CASCADE,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    rating NUMERIC(3,1) CHECK (rating >= 0 AND rating <= 10),
    comment TEXT
);

CREATE TABLE movie_actors (
    id SERIAL PRIMARY KEY,
    movie_id INTEGER REFERENCES movies(id) ON DELETE CASCADE,
    actor_id INTEGER REFERENCES actors(id) ON DELETE CASCADE
);

-- Индекс для поиска фильмов по названию
CREATE INDEX idx_movie_title ON movies(title);

-- Представление для топ-рейтинговых фильмов
CREATE VIEW top_rated_movies AS
SELECT id, title, year, rating
FROM movies
WHERE rating IS NOT NULL
ORDER BY rating DESC
LIMIT 10;