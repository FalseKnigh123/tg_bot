import datetime

import sqlalchemy

from tg_bot.data.db_session import SqlAlchemyBase


class Country(SqlAlchemyBase):
    __tablename__ = 'country'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    fullname = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    english = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    alpha2 = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    alpha3 = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    iso = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    location = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    location_precise = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    created_date = sqlalchemy.Column(sqlalchemy.DateTime,
                                     default=datetime.datetime.now)

