import sqlalchemy
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import sessionmaker, scoped_session

import config


app = Flask(__name__)
app.config.from_object('config.Config')
db = SQLAlchemy(app)
client = app.test_client()

from app import view


engine = sqlalchemy.create_engine(f'postgresql+psycopg2://postgres:admin@127.0.0.1:5432/some_db')
session = scoped_session(sessionmaker(
            bind=engine,
            autocommit=True,
            autoflush=True,
            enable_baked_queries=False,
            expire_on_commit=True
        ))

from app.models import *
