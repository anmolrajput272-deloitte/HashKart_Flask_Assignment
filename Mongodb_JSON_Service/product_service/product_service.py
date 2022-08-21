from Config import product_db
from pymongo.collection import ObjectId
from flask import request, jsonify
import function_helper
from flask import Flask
from Config import JSONEncoder
from settings import *

app = Flask(__name__)
app.json_encoder = JSONEncoder

@app.route('/get_all_products')
def get_all_product():
    return jsonify({"products":list(product_db.find())})

@app.route('/get_product_by_id/<string:id>')
def get_product_by_id(id):
    return jsonify(product_db.find_one({"_id":ObjectId(id)}))

@app.route('/get_my_products')
def get_my_products():
    id = function_helper.get_id_from_jwt(request.headers.get('Authorization'))
    return jsonify({"products":list(product_db.find({"seller_id": id}))})

@app.route('/get_my_products_id/<string:seller_id>')
def get_all_products_id(seller_id):
    return jsonify({"product_ids":list(product_db.find({"seller_id":seller_id},{"_id":1}))})

@app.route('/delete_all_products/<string:seller_id>',methods=['DELETE'])
def delete_all_products(seller_id):
    response = get_all_products_id(seller_id).json
    all_product_ids = []
    for item in response["product_ids"]:
        all_product_ids.append(item["_id"])
    for product_id in all_product_ids:
        product_db.delete_one({"_id":ObjectId(product_id)})
    print("All Deleted")
    return jsonify({"message":"successful"})
    # return r.json()

@app.route('/insert_product',methods=['POST'])
def insert_product():
    data = request.json
    id = function_helper.get_id_from_jwt(request.headers.get('Authorization'))
    data["seller_id"] = id
    return jsonify({"_id":str(product_db.insert_one(data).inserted_id)})

@app.route('/update_product/<string:product_id>',methods=['PUT'])
def update_product(product_id):
    data = request.json
    product_db.update_one({"_id":ObjectId(product_id)},{"$set":data})
    return jsonify({"message": "successful"})

@app.route('/product/filter',methods=['POST'])
def query_():

    data = request.json

    category_arr = []
    if 'via_category' in data:
        for item in data['via_category']:
            category_arr.append({"categories":item})

    range_arr = []
    if 'via_range' in data:
        for item in data['via_range']:
            range_arr.append({item['field']:{"$gte":item['range']['start'],"$lt":item['range']['end']}})

    sort_arr = []
    if 'sort' in data:
        for item in data['sort']:
            sort_arr.append((item['field'],item['type']))

    # data = product_db.find({ "$and": [{"$or": [{"categories": "xiaomi"}, {"categories": "redmi"}]} ,
    #                                   {"$and": [{"price": {"$gte": 9999,"$lt": 17000}} ]} ] })

    query = ''
    if len(category_arr) and len(range_arr):
        query = {"$and": [{"$or": category_arr}, {"$and": range_arr}]}
    elif len(category_arr):
        query = {"$or": category_arr}
    elif len(range_arr):
        query = {"$and": range_arr}
    else:
        query = {}

    data = ''
    if len(sort_arr):
        data = product_db.find(query).sort(sort_arr)
    else:
        data = product_db.find(query)

    # print(query)

    return jsonify({"Result":list(data)})

    # return jsonify({"message":"hello"})

@app.route('/increment_times_solid_of_product_ids',methods=['POST'])
def increment_times_solid_of_product_ids():
    products = request.json['products']
    for product in products:
        product_db.update_one({"_id":ObjectId(product["product_id"])},
                              {"$inc":{"quantity_left":product["product_count"]*-1,
                                       "times_sold":product["product_count"]}})
    return jsonify({"message":"Product IDs Updated"})

if __name__ == "__main__":
    app.run()