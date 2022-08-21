from Config import db, seller_db, user_db, JSONEncoder
from flask import Flask, request, jsonify
import Security
import function_helper
from pymongo.collection import ObjectId
from settings import *
import httpx

app = Flask("user_service")
app.json_encoder = JSONEncoder

@app.route('/register/<string:user_type>',methods=['POST'])
def seller_register(user_type):
    data = request.json
    if db[user_type].find_one({"email":data["email"]}) is None:
        id = db[user_type].insert_one(data).inserted_id
        return jsonify(db[user_type].find_one({"_id":id}))
    return jsonify({"message": "Seller with this Email Already exists"}),400

@app.route('/login/<string:user_type>',methods=['POST'])
def seller_login(user_type):
    # print(request.headers)
    data = request.json
    return Security.login(data,user_type)

@app.route('/delete_user/<string:user_id>',methods=['DELETE'])
def delete_user(user_id):
    # cart_service.delete_cart_by_user_id(user_id)
    httpx.delete(cart_service_url+"/delete_cart_by_user_id/"+user_id)
    # user_address_service.delete_addresses_by_userid(user_id)
    httpx.delete(user_address_service_url+"/delete_user_addresses/"+user_id)
    # user_payment_service.delete_payment_details_by_userid(user_id)
    httpx.delete(user_payment_service_url+"/delete_user_payment_details/"+user_id)
    user_db.delete_one({"_id":ObjectId(user_id)})
    return jsonify({"message":"User Deleted"})

@app.route('/delete_seller/<string:seller_id>',methods=['DELETE'])
def delete_seller(seller_id):
    data = httpx.get(product_service_url+"/get_my_products_id/"+seller_id).json()
    print(data)
    httpx.post(cart_service_url+"/delete_products_from_carts",json=dict(data)).json()
    httpx.delete(product_service_url + "/delete_all_products/" + seller_id).json()
    seller_db.delete_one({"_id":ObjectId(seller_id)})
    return jsonify({"message":"seller deleted"})

@app.route('/sellers')
def get_all_sellers():
    return jsonify({"Sellers":list(seller_db.find())})

@app.route('/users')
def get_all_users():
    return jsonify({"Users": list(user_db.find())})

@app.route('/create_index',methods=['POST'])
def create_index():
    data = request.json
    print(data)
    # db[data["table"]].create_index([("user_id",1),("products.product_id",1)])
    db[data["table"]].create_index(data["query"])
    return db[data["table"]].index_information()

@app.route('/get_user_id')
def get_id_from_user_jwt():
    return function_helper.get_id_from_jwt(request.headers.get('Authorization'))

@app.route('/get_seller_id')
def get_id_from_seller_jwt():
    return function_helper.get_id_from_jwt(request.headers.get('Authorization'))

@app.route("/delete-table/<string:table>")
def delete_table(table):
    db[table].drop()
    return jsonify({"message":"successful"}), 200

@app.route("/test_api",methods=['POST'])
def test_api():
    return jsonify({"message":"successful"})

if __name__ == "__main__":
    app.run()