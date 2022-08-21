from Config import seller_db
from pymongo.collection import ObjectId
from flask import request, jsonify
import function_helper
from flask import Flask
from Config import JSONEncoder
from settings import *

app = Flask(__name__)
app.json_encoder = JSONEncoder

@app.route('/seller/update_address',methods=['PUT'])
def update_seller_address():
    values = {"$set":{"address":request.json}}
    filter = {"_id":ObjectId(function_helper.get_id_from_jwt(request.headers.get('Authorization')))}
    seller_db.update_one(filter,values)
    return jsonify({"message":"successful"})

@app.route('/seller/get_my_address')
def get_my_seller_addresses():
    token = function_helper.get_id_from_jwt(request.headers.get('Authorization'))
    return jsonify({"address":seller_db.find_one({"_id": ObjectId(token)})['address']})

if __name__ == "__main__":
    app.run()