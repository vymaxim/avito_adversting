import sqlalchemy
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy_utils import database_exists, create_database

import config


app = Flask(__name__)
app.config.from_object('config.Config')
db = SQLAlchemy(app)
client = app.test_client()


from app import view


engine = sqlalchemy.create_engine(f'postgresql+psycopg2://postgres:postgres@mypostgres:5432/some_db')
if not database_exists(engine.url):
    create_database(engine.url)
session = scoped_session(sessionmaker(
            bind=engine,
            autocommit=True,
            autoflush=True,
            enable_baked_queries=False,
            expire_on_commit=True
        ))

from app.models import *
