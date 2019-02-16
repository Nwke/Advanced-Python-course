import csv
import re

import pymongo
from pymongo import MongoClient
from datetime import datetime

client = MongoClient()
songs_db = client['song']
song_collection = songs_db['song']


def _convert(data):
    month, day = data.split('.')[::-1]
    year = datetime.now().year

    return f'{year}-{month}-{day}'


def read_data(csv_file, db):
    """
    Load data into DB from CSV file
    """

    with open(csv_file, encoding='utf8') as csvfile:
        all_songs = []
        reader = csv.DictReader(csvfile)
        for row in reader:
            all_songs.append({
                'artist': row['Исполнитель'],
                'price': int(row['Цена']),
                'place': row['Место'],
                'date': _convert(row['Дата'])
            })

        return db.song.insert_many(all_songs)


def find_cheapest(db):
    """
    Search cheapest tickets
    """

    return db.song.find().sort([('price', pymongo.ASCENDING)])


def find_by_name(name, db):
    """
    Search field artist by substring
    """

    regexp = re.compile(rf'\w*{name}\w*')

    return db.song.find({'artist': regexp}).sort([('price', pymongo.ASCENDING)])


def event_by_time(db, start_time, end_time):
    return db.song.find({'date': {'$gte': start_time, '$lte': end_time}})


if __name__ == '__main__':
    read_data('artists.csv', songs_db)

    for event in list(find_cheapest(songs_db)):
        print(event)

    year = datetime.now().year
    start = f'{year}-07-01'
    end = f'{year}-07-30'

    for event in list(event_by_time(songs_db, start, end)):
        print(event)
