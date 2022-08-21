import json

from Config import order_db
from bson import json_util
from flask import request, jsonify
import function_helper
from flask import Flask
from Config import JSONEncoder
from settings import *
import httpx

app = Flask(__name__)
app.json_encoder = JSONEncoder

@app.route('/get_all_orders')
def get_all_orders():
    return jsonify({"Orders": list(order_db.find())})

@app.route('/get_my_orders')
def get_my_orders():
    id = function_helper.get_id_from_jwt(request.headers.get('Authorization'))
    return jsonify({"Orders":list(order_db.find({"user_id": id}))})

def insert(data):
    id = order_db.insert_one(data).inserted_id
    return jsonify(json.loads(json_util.dumps({
        "message":"Checkout Successful",
        "order_id": str(id),
        "order_details":data
    }))), 200

@app.route('/checkout',methods=['POST'])
def checkout():
    data = request.json
    if "payment_details_id" not in data:
        return jsonify({"message":"Checkout Failed, No Payment Details Id Given"}), 406

    # payment_details = get_payment_details_by_id(data["payment_details_id"]).json
    payment_details = httpx.get(user_payment_service_url+"/get_payment_details_by_id/"+data["payment_details_id"]).json()

    if payment_details is None:
        return jsonify({"message":"Payment ID Invalid"})

    id = function_helper.get_id_from_jwt(request.headers.get('Authorization'))
    # cart_ = get_cart_by_user_id(id).json

    cart_ = httpx.get(cart_service_url+"/get_cart_by_user_id/"+id).json()

    if cart_ is None:
        return jsonify({"message":"Checkout Failed, No Products in cart"}), 406

    if "coupon_code" in data:
        # validate_coupon_ = validate_coupon(data["coupon_code"],cart_["cart_value"]).json

        validate_coupon_ = httpx.get(coupon_service_url+"/validate_coupon/{}/{}".format(data["coupon_code"],cart_["cart_value"])).json()
        if validate_coupon_["is_valid"] is True:
            cart_["discounted_price"]=cart_["cart_value"]-validate_coupon_["discount_price"]
            cart_["coupon_applied"]=data["coupon_code"]

    # delete_cart_by_user_id(id).json
    httpx.delete(cart_service_url+"/delete_cart_by_user_id/"+id).json()
    cart_1 = {"products":cart_["products"]}
    print(cart_1)
    httpx.post(product_service_url+"/increment_times_solid_of_product_ids",json=cart_1)
    del cart_["_id"]
    cart_["payment_details"]=payment_details

    return insert(cart_)

if __name__ == "__main__":
    app.run()