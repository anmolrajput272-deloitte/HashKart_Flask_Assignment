from Config import app
from flask import request
import Security
from Security import get_headers
from settings import *
import httpx

@app.route('/get_all_carts')
def get_all_carts():
    return httpx.get(cart_service_url+"/get_all_carts",headers=get_headers()).json()

@app.route('/get_my_cart')
@Security.user_token_required
def get_my_cart():
    return httpx.get(cart_service_url+"/get_my_cart",headers=get_headers()).json()

@app.route('/add_product/<string:product_id>',methods=['POST'])
@Security.user_token_required
def add_product_to_cart(product_id):
    return httpx.post(cart_service_url+"/add_product/"+product_id,headers=get_headers()).json()

@app.route('/delete_product/<string:product_id>',methods=['DELETE'])
@Security.user_token_required
def delete_product_from_cart(product_id):
    return httpx.delete(cart_service_url+"/delete_product/"+product_id,headers=get_headers()).json()

@app.route('/delete_cart_by_user_id/<string:user_id>',methods=['DELETE'])
def delete_cart_by_user_id(user_id):
    return httpx.delete(cart_service_url+"/delete_cart_by_user_id/"+user_id,headers=get_headers()).json()

@app.route('/get_cart_by_user_id/<string:user_id>')
def get_cart_by_user_id(user_id):
    return httpx.get(cart_service_url+"/get_cart_by_user_id/"+user_id,headers=get_headers()).json()

@app.route('/delete_user_cart/<string:user_id>',methods=['DELETE'])
def delete_user_cart(user_id):
    return httpx.delete(cart_service_url+"/delete_user_cart/"+user_id,headers=get_headers()).json()

@app.route('/delete_products_from_carts',methods=['POST'])
def delete_products_from_all_carts():
    return httpx.post(cart_service_url+"/delete_products_from_carts",json=request.json,headers=get_headers())