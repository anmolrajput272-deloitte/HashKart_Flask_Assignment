from Config import app
from flask import request
import Security
from Security import get_headers
from settings import *
import httpx

@app.route('/register/<string:user_type>',methods=['POST'])
def seller_register(user_type):
    return httpx.post(user_service_url+"/register/"+user_type,json=request.json,headers=get_headers()).json()

@app.route('/login/<string:user_type>',methods=['POST'])
def seller_login(user_type):
    return httpx.post(user_service_url+"/login/"+user_type,json=request.json,headers=get_headers()).json()

@app.route('/delete_user/<string:user_id>',methods=['DELETE'])
def delete_user(user_id):
    return httpx.delete(user_service_url+"/delete_user/"+user_id,headers=get_headers()).json()

@app.route('/delete_seller/<string:seller_id>',methods=['DELETE'])
def delete_seller(seller_id):
    return httpx.delete(user_service_url+"/delete_seller/"+seller_id,headers=Security.get_headers()).json()

@app.route('/sellers')
@Security.seller_token_required
def get_all_sellers():
    return httpx.get(user_service_url+"/sellers",headers=get_headers()).json()

@app.route('/users')
@Security.user_token_required
def get_all_users():
    return httpx.get(user_service_url+"/users",headers=get_headers()).json()

@app.route('/create_index',methods=['POST'])
def create_index():
    headers_ = {}
    if "Authorization" in request.headers:
        headers_["Authorization"] = request.headers.get('Authorization')
    return httpx.post(user_service_url + "/create_index",data=request.json,headers=get_headers()).json()

@app.route('/get_user_id')
@Security.user_token_required
def get_id_from_user_jwt():
    headers_ = {}
    if "Authorization" in request.headers:
        headers_["Authorization"] = request.headers.get('Authorization')
    return httpx.get(user_service_url+"/get_user_id",headers=get_headers()).json()

@app.route('/get_seller_id')
@Security.seller_token_required
def get_id_from_seller_jwt():
    headers_ = {}
    if "Authorization" in request.headers:
        headers_["Authorization"] = request.headers.get('Authorization')
    return httpx.get(user_service_url+"/get_seller_id",headers=get_headers()).json()

@app.route("/delete-table/<string:table>",methods=['DELETE'])
def delete_table(table):
    return httpx.delete(user_service_url+"/delete-table/"+table,headers=get_headers()).json()


@app.route("/test_api",methods=['POST'])
def test_api():
    return httpx.post(user_service_url+"/test_api",json=request.json,headers=get_headers()).json()

