from Config import user_payment_db
from pymongo.collection import ObjectId
from flask import request, jsonify
import function_helper
from flask import Flask
from Config import JSONEncoder
from settings import *

app = Flask(__name__)
app.json_encoder = JSONEncoder

@app.route('/user/get_all_payment_details')
def get_all_user_payment_details():
    return jsonify({"payment_details":list(user_payment_db.find())})

@app.route('/user/update_payment/<string:payment_id>',methods=['PUT'])
def update_user_payment_details(payment_id):
    values = {"$set":request.json}
    filter = {"_id":ObjectId(payment_id)}
    user_payment_db.update_one(filter,values)
    return jsonify({"message":"successful"})

@app.route('/user/get_my_payment_details')
def get_my_user_payment_details():
    id = function_helper.get_id_from_jwt(request.headers.get('Authorization'))
    return jsonify({"payment_details":list(user_payment_db.find({"user_id": id}))})

@app.route('/user/insert_payment_details',methods=['POST'])
def insert_user_payment_details():
    response = request.json
    response["user_id"] = function_helper.get_id_from_jwt(request.headers.get('Authorization'))
    return jsonify({"_id":str(user_payment_db.insert_one(response).inserted_id)})

@app.route('/get_payment_details_by_id/<string:id>')
def get_payment_details_by_id(id):
    return jsonify(user_payment_db.find_one({"_id":ObjectId(id)}))

@app.route('/delete_payment_details/<string:id>',methods=['DELETE'])
def delete_payment_details_by_id(id):
    user_payment_db.delete_one({"_id":ObjectId(id)})
    return jsonify({"message":"Payment Details Deleted"})

@app.route('/delete_user_payment_details/<string:user_id>',methods=['DELETE'])
def delete_payment_details_by_userid(user_id):
    user_payment_db.delete_many({"user_id": user_id})
    return jsonify({"message":"All Payment Details Of User Deleted"})

if __name__ == "__main__":
    app.run()