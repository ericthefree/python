# ./api_app/resources/db
# Initialize the database
from pymongo import MongoClient

# Setup our app to connect to the mongo database

# LOCAL RUN UNCOMMENT THE LINE BELOW FOR CONNECTING TO THE DATABASE SERVER
mongo_client = MongoClient('mongodb://mongodbuser:password_unsecure@localhost:27017')

# UNCOMMENT THE NEXT LINE IF YOU ARE REBUILDING THE IMAGE
# mongo_client = MongoClient('mongodb://mongodbuser:password_unsecure@mongo_db:27017')

mongo_db = mongo_client.api_db
mongo_col = mongo_db["servers"]
