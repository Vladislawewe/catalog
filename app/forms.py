from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length, ValidationError
from .models import User

class RegistrationForm(FlaskForm):
    first_name = StringField('Имя', validators=[DataRequired(), Length(max=50)])
    last_name = StringField('Фамилия', validators=[DataRequired(), Length(max=50)])
    email = StringField('Email', validators=[DataRequired(), Email(), Length(max=120)])
    password = PasswordField('Пароль', validators=[DataRequired(), Length(min=6, max=128)])
    submit = SubmitField('Зарегистрироваться')

    def validate_email(self, email):
        # Проверка уникальности email
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Этот email уже зарегистрирован.')