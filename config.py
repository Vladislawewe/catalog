import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'your_secret_key')
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL',
        'postgresql://postgres:postgres@localhost:5432/catalog'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False