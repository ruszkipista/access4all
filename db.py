import os
# Support for mongodb+srv:// URIs requires dnspython:
#!pip install dnspython pymongo
import pymongo
import json
from datetime import datetime
from werkzeug.security import generate_password_hash
from werkzeug.utils import secure_filename
import certificate
from flask import g, session
from bson.objectid import ObjectId
from bson.binary import Binary

# envDB.py should exist only in Development
if os.path.exists("envDB.py"):
    import envDB

# MongoDB parameters
dbConfig = {}
dbConfig["OS_DATA_PATH"] = os.environ.get("OS_DATA_PATH", "./static/data/")
dbConfig["MONGO_CLUSTER"] = os.environ.get("MONGO_CLUSTER")
dbConfig["MONGO_DB_NAME"] = os.environ.get("MONGO_DB_NAME")
dbConfig["MONGO_URI"] = f"mongodb+srv:" + \
    f"//{os.environ.get('MONGO_DB_USER')}" + \
    f":{os.environ.get('MONGO_DB_PASS')}" + \
    f"@{dbConfig['MONGO_CLUSTER']}" + \
    f".ueffo.mongodb.net" + \
    f"/{dbConfig['MONGO_DB_NAME']}" + \
    f"?retryWrites=true&w=majority"

# MongoDB
# =========
def get_db_collection(collectionName):
    conn = getattr(g, '_database_mongo', None)
    if conn is None:
        try:
            conn = g._database_mongo = pymongo.MongoClient(
                dbConfig["MONGO_URI"], tlsCAFile=certifi.where())
        except pymongo.errors.ConnectionFailure as e:
            print(f"Could not connect to MongoDB {collectionName}: {e}")
            return None
    return conn[collectionName]


def close_db_connection(exception):
    db = getattr(g, '_database_mongo', None)
    if db is not None:
        db.close()
