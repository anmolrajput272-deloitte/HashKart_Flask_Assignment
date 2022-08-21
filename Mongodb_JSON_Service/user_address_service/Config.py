import pymongo
from flask import Flask
import json
from bson import ObjectId

myclient = pymongo.MongoClient("localhost",27017)
db = myclient.mydb

user_address_db = db.user_address

class JSONEncoder(json.JSONEncoder):
    ''' extend json-encoder class'''
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)

# use the modified encoder class to handle ObjectId & datetime object while jsonifying the response.