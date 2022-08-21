from Config import app
import Security
from flask import request
from settings import *
import httpx

@app.route('/get_all_products')
def get_all_product():
    return httpx.get(product_service_url+"/get_all_products",headers=Security.get_headers()).json()

@app.route('/get_product_by_id/<string:id>')
def get_product_by_id(id):
    return httpx.get(product_service_url+"/get_product_by_id/"+id,headers=Security.get_headers()).json()

@app.route('/get_my_products')
@Security.seller_token_required
def get_my_products():
    return httpx.get(product_service_url+"/get_my_products",headers=Security.get_headers()).json()

@app.route('/get_my_products_id/<string:seller_id>')
def get_all_products_id(seller_id):
    return httpx.get(product_service_url+"/get_my_products_id/"+seller_id,headers=Security.get_headers()).json()

@app.route('/delete_all_products/<string:seller_id>',methods=['DELETE'])
def delete_all_products(seller_id):
    return httpx.delete(product_service_url+"/delete_all_products/"+seller_id,headers=Security.get_headers()).json()

@app.route('/insert_product',methods=['POST'])
@Security.seller_token_required
def insert_product():
    return httpx.post(product_service_url+"/insert_product",json=request.json,headers=Security.get_headers()).json()

@app.route('/update_product/<string:product_id>',methods=['PUT'])
def update_product(product_id):
    return httpx.put(product_service_url+"/update_product/"+product_id,json=request.json,headers=Security.get_headers()).json()

@app.route('/product/filter',methods=['POST'])
def query_():
    return httpx.post(product_service_url+"/product/filter",json=request.json,headers=Security.get_headers()).json()