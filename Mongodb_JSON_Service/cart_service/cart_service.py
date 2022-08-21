from Config import cart_db
from pymongo.collection import ObjectId
from flask import request, jsonify
import function_helper
from flask import Flask
from Config import JSONEncoder
from settings import *
import httpx

app = Flask("cart_service")
app.json_encoder = JSONEncoder

@app.route('/get_all_carts')
def get_all_carts():
    return jsonify({"Carts":list(cart_db.find())})

@app.route('/get_my_cart')
def get_my_cart():
    id = function_helper.get_id_from_jwt(request.headers.get('Authorization'))
    data = cart_db.find_one({"user_id":id})
    return jsonify(data) if data is not None else jsonify({"message":"no items in cart"})

@app.route('/add_product/<string:product_id>',methods=['POST'])
def add_product_to_cart(product_id):
    id = function_helper.get_id_from_jwt(request.headers.get('Authorization'))
    # product_ = get_product_by_id(product_id).json
    product_ = httpx.get(product_service_url+"/get_product_by_id/"+product_id).json()

    if product_ is None:
        return jsonify({"message":"Invalid Product_ID"})

    query = {"user_id":id,"products.product_id":product_id}
    cart_element = cart_db.find_one(query)

    if cart_element is not None:
        cart_db.update_one(query,{ "$inc":{"cart_value":product_["price"],"products.$.product_count":1,"products.$.product_value":product_["price"]} })
    elif cart_db.find_one({"user_id":id}) is not None:
        cart_db.update_one({"user_id":id},{"$push":{"products":{ "product_id":product_id, "product_count":1, "product_value":product_["price"] }},
                                           "$inc":{"cart_value":product_["price"]} })
    else:
        cart_db.insert_one({"user_id":id,"products":[{"product_id":product_id,"product_count":1, "product_value":product_["price"]}],"cart_value":product_["price"]})

    return jsonify({"message":"successful"})

@app.route('/delete_product/<string:product_id>',methods=['DELETE'])
def delete_product_from_cart(product_id):
    id = function_helper.get_id_from_jwt(request.headers.get('Authorization'))
    # product_ = get_product_by_id(product_id).json
    product_ = httpx.get(product_service_url + "/get_product_by_id/" + product_id).json()

    if product_ is None:
        return {"message":"Invalid Product_ID"}

    query = {"user_id":id,"products.product_id":product_id}
    cart_element = cart_db.find_one(query)

    if cart_element is not None:
        for item in cart_element['products']:
            if item['product_id']==product_id:
                if item['product_count']==1:
                    cart_db.update_one(query,
                                       {"$pull": {"products": {"product_id": product_id}},"$inc":{"cart_value": product_["price"] * -1,
                                                                                                  "products.$.product_value":product_["price"] * -1}})
                else:
                    cart_db.update_one(query,
                                       {"$inc": {"cart_value": product_["price"] * -1, "products.$.product_count": -1,
                                                 "products.$.product_value":product_["price"] * -1}})
                break
        return jsonify({"message":"successful"})
    return jsonify({"message":"Product not available in cart"})

@app.route('/delete_cart_by_user_id/<string:user_id>',methods=['DELETE'])
def delete_cart_by_user_id(user_id):
    cart_db.delete_one({"user_id":user_id})
    return jsonify({"message":"successsful"})

@app.route('/get_cart_by_user_id/<string:user_id>')
def get_cart_by_user_id(user_id):
    return jsonify(cart_db.find_one({"user_id":user_id}))

@app.route('/delete_user_cart/<string:user_id>',methods=['DELETE'])
def delete_user_cart(user_id):
    cart_db.delete_one({"user_id":user_id})
    return jsonify({"message":"successsful"})


@app.route('/delete_products_from_carts',methods=['POST'])
def delete_products_from_all_carts():
    product_id_arr = request.json["product_ids"]
    product_id_arr_dict = {''}
    product_id_arr_arr = []
    for item in product_id_arr:
        product_id_arr_arr.append(item["_id"])
        product_id_arr_dict.add(item["_id"])
    print(product_id_arr_arr)
    response = cart_db.find({"products.product_id":{"$in":product_id_arr_arr}})

    new_price = {}
    cleared_carts = {''}
    for item in response:
        sum = 0
        for product in item['products']:
            if product['product_id'] in product_id_arr_dict:
                sum += product["product_value"]
        new_price[item['_id']] = item["cart_value"]-sum
        if new_price[item['_id']]==0:
            cleared_carts.add(item['_id'])

    for key in new_price:
        if key not in cleared_carts:
            cart_db.update_one({"_id":ObjectId(key)},{
                "$pull":{
                    "products":{
                        "product_id":{
                            "$in":product_id_arr_arr
                        }
                    }
                },
                "$set":{
                    "cart_value":new_price[key]
                }
            })

        else:
            cart_db.delete_one({"_id": ObjectId(key)})

    return jsonify({"message":"Products Deleted"})

if __name__ == "__main__":
    app.run()