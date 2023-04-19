import csv
import sys

from data import db_session
from data.countries import Country


def loadTable(table_name):
    with open(table_name, encoding="utf8") as csvfile:
        reader = csv.reader(csvfile, delimiter='\t', quotechar='"')
        title = next(reader)
        return list(reader)

db_sess = db_session.create_session()

for cont in loadTable('www.artlebedev.ru.csv'):
    country = Country()
    country.name = cont[0]
    country.fullname = cont[1]
    country.english = cont[2]
    country.alpha2 = cont[3]
    country.alpha2 = cont[4]
    country.iso = cont[5]
    country.location = cont[6]
    country.location_precise = cont[7]
db_sess.add(country)
db_sess.commit()



loadTable('www.artlebedev.ru.csv')
