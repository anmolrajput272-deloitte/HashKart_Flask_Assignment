import pymongo
from flask import Flask
import json
from bson import ObjectId

myclient = pymongo.MongoClient("localhost",27017)
db = myclient.mydb

order_db = db.order

class JSONEncoder(json.JSONEncoder):
    ''' extend json-encoder class'''
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)

# use the modified encoder class to handle ObjectId & datetime object while jsonifying the response.