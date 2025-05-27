from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, FloatField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, NumberRange

class RegistrationForm(FlaskForm):
    first_name = StringField('Имя', validators=[DataRequired()])
    last_name = StringField('Фамилия', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    confirm_password = PasswordField('Подтвердите пароль', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Зарегистрироваться')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    submit = SubmitField('Войти')

class ReviewForm(FlaskForm):
    rating = FloatField('Рейтинг (0-10)', validators=[DataRequired(), NumberRange(min=0, max=10)])
    comment = TextAreaField('Комментарий')
    submit = SubmitField('Отправить отзыв')