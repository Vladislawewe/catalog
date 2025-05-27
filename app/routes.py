from flask import Blueprint, render_template, redirect, url_for, flash
from .forms import RegistrationForm
from .models import Movie, Director, Actor, User, Review, Genre
from . import db

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    movies = Movie.query.limit(10).all()
    return render_template('index.html', movies=movies)

@bp.route('/movies')
def movies():
    movies = Movie.query.all()
    return render_template('movies.html', movies=movies)

@bp.route('/directors')
def directors():
    directors = Director.query.all()
    return render_template('directors.html', directors=directors)

@bp.route('/actors')
def actors():
    actors = Actor.query.all()
    return render_template('actors.html', actors=actors)

@bp.route('/users')
def users():
    users = User.query.all()
    return render_template('users.html', users=users)

@bp.route('/reviews')
def reviews():
    reviews = Review.query.all()
    return render_template('reviews.html', reviews=reviews)

@bp.route('/top-rated')
def top_rated_movies():
    movies = Movie.query.order_by(Movie.rating.desc()).limit(10).all()
    return render_template('top_rated_movies.html', movies=movies)

@bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        new_user = User(
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            email=form.email.data
            # В реальном проекте тут еще и хэш пароля
        )
        db.session.add(new_user)
        db.session.commit()
        flash('Регистрация прошла успешно!', 'success')
        return redirect(url_for('main.index'))
    return render_template('register.html', form=form)