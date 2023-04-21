import csv
import sys


from data import db_session
from data.countries import Country


def loadTable(table_name):
    with open(table_name, encoding="utf8") as csvfile:
        reader = csv.reader(csvfile, delimiter=';', quotechar='"')
        title = next(reader)
        return list(reader)


def create_table():
    db_sess = db_session.create_session()
    db_sess.query(Country).filter(True).delete()
    db_sess.commit()

    for cont in loadTable('for_bd.csv'):
        country = Country()
        country.name = cont[0]
        country.fullname = cont[1]
        country.english = cont[2]
        country.alpha2 = cont[3]
        country.location = cont[4]
        country.location_precise = cont[5]
        country.capital = cont[6]
        country.currentcy = cont[7]
        country.square = float(cont[8]) if cont[8] else 0
        country.language = cont[9]
        country.population = int(cont[10]) if cont[10] else 0
        db_sess.add(country)
    db_sess.commit()

