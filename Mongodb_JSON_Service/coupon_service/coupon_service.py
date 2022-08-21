from Config import coupon_db
from pymongo.collection import ObjectId
from flask import request, jsonify
import function_helper
from flask import Flask
from Config import JSONEncoder
from settings import *
import httpx

app = Flask(__name__)
app.json_encoder = JSONEncoder

@app.route('/update_coupon/<string:coupon_id>',methods=['PUT'])
def update_coupon(coupon_id):
    values = {"$set":request.json}
    filter = {"_id":ObjectId(coupon_id)}
    coupon_db.update_one(filter,values)
    return jsonify({"message":"successful"})

@app.route('/get_coupons')
def get_coupons():
    return jsonify({"Coupons":list(coupon_db.find())}), 200

@app.route('/insert_coupon',methods=['POST'])
def insert_coupon():
    return jsonify({"_id":str(coupon_db.insert_one(request.json).inserted_id)})

@app.route('/delete_coupon/<string:coupon_code>',methods=['DELETE'])
def delete_coupon(coupon_code):
    coupon = coupon_db.find_one({"code":coupon_code})
    if coupon is None:
        return {"message":"Coupon Not Present"}
    coupon_db.delete_one({"_id":coupon["_id"]})
    return {"message":"Coupon Deleted"}

@app.route('/validate_coupon/<string:coupon_code>/<int:cart_value>')
def validate_coupon(coupon_code, cart_value):
    coupon = coupon_db.find_one({"code":coupon_code})
    if coupon is not None and cart_value>=coupon["min_price"] and cart_value<=coupon["max_price"]:
        return jsonify({"is_valid": True, "discount_price": coupon["discount_price"], "message": "Coupon Code Valid"})
    if coupon is None:
        return jsonify({"is_valid": False, "discount_price": 0, "message": "Coupon Code Not Present"})
    return jsonify({"is_valid": False, "discount_price": 0, "message": "Coupon Code Not valid For Your Cart Value"})

@app.route('/validate_coupon/<string:coupon_code>')
def validate_coupon_for_cart(coupon_code):
    id = function_helper.get_id_from_jwt(request.headers.get('Authorization'))
    # cart_ = get_cart_by_user_id(id).json
    cart_ = httpx.get(cart_service_url+"/get_cart_by_user_id/"+id).json()
    if cart_ is None:
        return jsonify({"message":"No Products in cart"})
    return validate_coupon(coupon_code,cart_["cart_value"])

if __name__ == "__main__":
    app.run()