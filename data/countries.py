import datetime

import sqlalchemy

from data.db_session import SqlAlchemyBase


class Country(SqlAlchemyBase):
    __tablename__ = 'country'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    fullname = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    english = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    alpha2 = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    location = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    location_precise = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    capital = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    currentcy = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    square = sqlalchemy.Column(sqlalchemy.Float, nullable=False)
    language = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    population = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    created_date = sqlalchemy.Column(sqlalchemy.DateTime,
                                     default=datetime.datetime.now)


class Flag(SqlAlchemyBase):
    __tablename__ = 're'
    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    created_date = sqlalchemy.Column(sqlalchemy.DateTime,
                                     default=datetime.datetime.now)

