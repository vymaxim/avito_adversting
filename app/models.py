from sqlalchemy import Column, Integer, VARCHAR, DateTime, func
from sqlalchemy.ext.declarative import declarative_base

from app import *
from app import session

Base = declarative_base()
Base.query = session.query_property()


class Ads(Base):

    __tablename__ = 'ads'

    id = Column(Integer, autoincrement=True, nullable=False, primary_key=True)
    name = Column(VARCHAR(200), nullable=False)
    description = Column(VARCHAR(1000), nullable=True)
    price = Column(Integer, nullable=False)
    main_url = Column(VARCHAR(1000), nullable=True)
    url2 = Column(VARCHAR(1000), nullable=True)
    url3 = Column(VARCHAR(1000), nullable=True)
    data_create = Column(DateTime(timezone=True), default=func.now())

if not engine.dialect.has_table(engine, 'ads'):
    Base.metadata.tables[f'{Ads.__tablename__}'].create(engine)
