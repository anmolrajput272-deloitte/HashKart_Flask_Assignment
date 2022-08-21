from Config import app
import Security
from flask import request
from settings import *
import httpx

@app.route('/seller/update_address',methods=['PUT'])
@Security.seller_token_required
def update_seller_address():
    return httpx.put(seller_address_service_url+"/seller/update_address",json=request.json,headers=Security.get_headers()).json()

@app.route('/seller/get_my_address')
@Security.seller_token_required
def get_my_seller_addresses():
    return httpx.get(seller_address_service_url+"/seller/get_my_address",headers=Security.get_headers()).json()