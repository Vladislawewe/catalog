from flask import Flask, render_template, redirect, url_for, flash
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User
from flask import Flask

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost/movie_catalog?client_encoding=utf8'
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)

db.init_app(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

from forms import RegistrationForm, LoginForm, ReviewForm
from models import User, Movie, Review, Actor, MovieActor, Genre, Director


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/')
def index():
    movies = Movie.query.all()
    return render_template('index.html', movies=movies)


@app.route('/movies/<int:id>')
def movie_detail(id):
    movie = Movie.query.get_or_404(id)
    reviews = Review.query.filter_by(movie_id=id).all()
    actors = Actor.query.join(MovieActor).filter(MovieActor.movie_id == id).all()
    return render_template('movie_detail.html', movie=movie, reviews=reviews, actors=actors)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data)
        user = User(first_name=form.first_name.data, last_name=form.last_name.data,
                    email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Регистрация успешна! Пожалуйста, войдите.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            flash('Вход выполнен успешно!', 'success')
            return redirect(url_for('index'))
        flash('Неверный email или пароль.', 'danger')
    return render_template('login.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Вы вышли из системы.', 'success')
    return redirect(url_for('index'))


@app.route('/movies/<int:id>/review', methods=['GET', 'POST'])
@login_required
def add_review(id):
    movie = Movie.query.get_or_404(id)
    # Проверяем, оставил ли пользователь уже отзыв
    existing_review = Review.query.filter_by(movie_id=id, user_id=current_user.id).first()
    if existing_review:
        flash('Вы уже оставили отзыв на этот фильм.', 'warning')
        return redirect(url_for('movie_detail', id=id))

    form = ReviewForm()
    if form.validate_on_submit():
        review = Review(
            movie_id=id,
            user_id=current_user.id,
            rating=form.rating.data,
            comment=form.comment.data
        )
        db.session.add(review)
        db.session.commit()
        movie.update_rating()  # Обновляем рейтинг фильма
        flash('Отзыв успешно добавлен!', 'success')
        return redirect(url_for('movie_detail', id=id))
    return render_template('add_review.html', form=form, movie=movie)


if __name__ == '__main__':
    app.run(debug=True)