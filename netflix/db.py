import os

from pymongo import MongoClient


def get_db():
    if (db is not None):
        return db


try:
    if 'MONGO_URI' in os.environ:
        mongoClient = MongoClient(os.environ['MONGO_URI'])
    else:
        mongoClient = MongoClient('localhost:27017')

    db = mongoClient.netflix

    print("Successfully connected to DB")

except:
    print("Error Connecting to DB")
