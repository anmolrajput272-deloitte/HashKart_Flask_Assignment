from Config import app
from flask import request
import Security
from settings import *
import httpx

@app.route('/update_coupon/<string:coupon_id>',methods=['PUT'])
def update_coupon(coupon_id):
    return httpx.put(coupon_service_url+"/update_coupon/"+coupon_id,json=request.json,headers=Security.get_headers()).json()

@app.route('/get_coupons')
def get_coupons():
    return httpx.get(coupon_service_url+"/get_coupons",headers=Security.get_headers()).json()

@app.route('/insert_coupon',methods=['POST'])
def insert_coupon():
    return httpx.post(coupon_service_url+"/insert_coupon",json=request.json,headers=Security.get_headers()).json()

@app.route('/delete_coupon/<string:coupon_code>',methods=['DELETE'])
def delete_coupon(coupon_code):
    return httpx.delete(coupon_service_url+"/delete_coupon/"+coupon_code,headers=Security.get_headers()).json()

@app.route('/validate_coupon/<string:coupon_code>/<int:cart_value>')
def validate_coupon(coupon_code, cart_value):
    return httpx.get(coupon_service_url+"/validate_coupon/{}/{}".format(coupon_code,cart_value),headers=Security.get_headers()).json()

@app.route('/validate_coupon/<string:coupon_code>')
@Security.user_token_required
def validate_coupon_for_cart(coupon_code):
    return httpx.get(coupon_service_url+"/validate_coupon/"+coupon_code,headers=Security.get_headers()).json()
