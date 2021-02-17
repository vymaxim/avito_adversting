import os


class Config():
    DEBUG = True
    SECRET_KEY = 'YOUR_RANDOM_SECRET_KEY'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'postgresql+psycopg2://postgres:admin@localhost:5432/some_db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
