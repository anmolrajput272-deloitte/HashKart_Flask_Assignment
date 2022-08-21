from Config import app
import Security
from flask import request
from settings import *
import httpx

@app.route('/user/get_all_addresses')
def get_all_user_addresses():
    return httpx.get(user_address_service_url+"/user/get_all_addresses",headers=Security.get_headers()).json()

@app.route('/user/update_address/<string:address_id>',methods=['PUT'])
def update_user_address(address_id):
    return httpx.put(user_address_service_url+"/user/update_address/"+address_id,json=request.json,headers=Security.get_headers()).json()

@app.route('/user/get_my_addresses')
@Security.user_token_required
def get_my_user_addresses():
    return httpx.get(user_address_service_url+"/user/get_my_addresses",headers=Security.get_headers()).json()

@app.route('/user/insert_address',methods=['POST'])
@Security.user_token_required
def insert_user_address():
    print(request.json)
    return httpx.post(user_address_service_url+"/user/insert_address",json=request.json,headers=Security.get_headers()).json()

@app.route('/delete_address/<string:id>',methods=['DELETE'])
def delete_address_by_id(id):
    return httpx.delete(user_address_service_url+"/delete_address/"+id).json()

@app.route('/delete_user_addresses/<string:user_id>',methods=['DELETE'])
def delete_addresses_by_userid(user_id):
    return httpx.delete(user_address_service_url+"/delete_user_addresses/"+user_id).json()