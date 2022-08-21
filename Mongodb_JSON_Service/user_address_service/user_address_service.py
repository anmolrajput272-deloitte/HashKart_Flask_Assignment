from Config import user_address_db
from pymongo.collection import ObjectId
from flask import request, jsonify
import function_helper
from flask import Flask
from Config import JSONEncoder
from settings import *

app = Flask(__name__)
app.json_encoder = JSONEncoder

@app.route('/user/get_all_addresses')
def get_all_user_addresses():
    return jsonify({"addresses":list(user_address_db.find())})

@app.route('/user/update_address/<string:address_id>',methods=['PUT'])
def update_user_address(address_id):
    values = {"$set":request.json}
    filter = {"_id":ObjectId(address_id)}
    user_address_db.update_one(filter,values)
    return jsonify({"message":"successful"})

@app.route('/user/get_my_addresses')
def get_my_user_addresses():
    id = function_helper.get_id_from_jwt(request.headers.get('Authorization'))
    return jsonify({"addresses":list(user_address_db.find({"user_id": id}))})

@app.route('/user/insert_address',methods=['POST'])
def insert_user_address():
    response = request.json
    print(response)
    response["user_id"] = function_helper.get_id_from_jwt(request.headers.get('Authorization'))
    id = user_address_db.insert_one(response).inserted_id
    return jsonify(user_address_db.find_one({"_id":id}))

@app.route('/delete_address/<string:id>',methods=['DELETE'])
def delete_address_by_id(id):
    user_address_db.delete_one({"_id":ObjectId(id)})
    return jsonify({"message":"Address Deleted"})

@app.route('/delete_user_addresses/<string:user_id>',methods=['DELETE'])
def delete_addresses_by_userid(user_id):
    user_address_db.delete_many({"user_id": user_id})
    return jsonify({"message":"All Addresses Of The User Deleted"})

if __name__ == "__main__":
    app.run()