from Config import app
from flask import request
import Security
from settings import *
import httpx

@app.route('/get_all_orders')
def get_all_orders():
    return httpx.get(order_service_url+"/get_all_orders",headers=Security.get_headers()).json()

@app.route('/get_my_orders')
@Security.user_token_required
def get_my_orders():
    return httpx.get(order_service_url+"/get_my_orders",headers=Security.get_headers()).json()

@app.route('/checkout',methods=['POST'])
@Security.user_token_required
def checkout():
    return httpx.post(order_service_url+"/checkout",json=request.json,headers=Security.get_headers()).json()