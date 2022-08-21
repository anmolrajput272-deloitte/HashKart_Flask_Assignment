from flask import request, jsonify
import jwt
import datetime
from settings import secret_key
from Config import user_db,seller_db

def authenticate(email,password,user_type):
    response = None
    if user_type=="seller":
        response = seller_db.find_one({"email":email})
    else:
        response = user_db.find_one({"email": email})
    if response is not None and response["password"] == password:
        return {"authenticated":True,"_id":str(response["_id"])}
    return {"authenticated":False}


def login(data,user_type_required):
    response = authenticate(data["email"],data["password"],user_type_required)
    if not response["authenticated"]:
        return jsonify({"message":"Incorrect Credentials"}), 400
    print(response)
    token = jwt.encode({'user' : data['email'],
                        'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=300),
                        'user_type':user_type_required,
                        '_id':response['_id']},secret_key)
    return jsonify({'token':token.decode('UTF-8')}), 200


def auth():
    return jsonify({"message":"Authentication Successful"}) , 200
