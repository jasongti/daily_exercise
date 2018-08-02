import requests
import pymongo
import time

client = pymongo.MongoClient()
db = client.douban
collections = db.movies
col_casts = db.casts


def get_cast(id):
    if not id:
        return
    print 'fetching:', id
    try:
        url = 'https://api.douban.com/v2/movie/celebrity/' + str(id)
        data = requests.get(url).json()
        print 'updating:', id
        col_casts.update_one({'id': data['id']}, {'$set': data}, upsert=True)
        print 'done:', id
    except Exception as e:
        print e, id

for i in collections.find():
    for cast in i['casts']:
        print cast['name'], cast['id']
        get_cast(cast['id'])
        time.sleep(1.5)
