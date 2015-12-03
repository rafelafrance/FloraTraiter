# use this like so: python words.py | sort | uniq > words.txt

import csv
import re
from collections import namedtuple

base_name = 'vntraits110715'
in_name = base_name

Row = namedtuple(
    'Row',
    ('occurrenceid institutionid collectionid datasetid '
     'institutioncode collectioncode catalognumber '
     'scientificname class_ individualcount sex lifestage '
     'dynamicproperties occurrenceremarks fieldnotes'))

punct = re.compile(r'[\s\d!@#$%^&*()+=|\\\]\[}{\'";/?:><,]-]+')


def main():
    with open(in_name, 'rb') as in_file:
        reader = csv.reader(in_file)
        row = reader.next()   # Header row
        for raw_row in reader:
            row = Row._make(raw_row)
            words = punct.split(row.dynamicproperties)
            words.extend(punct.split(row.occurrenceremarks))
            words.extend(punct.split(row.fieldnotes))
            for word in words:
                word = word.lower()
                if word:
                    print word


if __name__ == '__main__':
    main()