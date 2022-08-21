from Config import app
import Security
from flask import request
from settings import *
import httpx

@app.route('/user/get_all_payment_details')
def get_all_user_payment_details():
    return httpx.get(user_payment_service_url+'/user/get_all_payment_details',headers=Security.get_headers()).json()

@app.route('/user/update_payment/<string:payment_id>',methods=['PUT'])
def update_user_payment_details(payment_id):
    return httpx.put(user_payment_service_url+"/user/update_payment/"+payment_id,json=request.json,headers=Security.get_headers()).json()

@app.route('/user/get_my_payment_details')
@Security.user_token_required
def get_my_user_payment_details():
    return httpx.get(user_payment_service_url+"/user/get_my_payment_details",headers=Security.get_headers()).json()

@app.route('/user/insert_payment_details',methods=['POST'])
@Security.user_token_required
def insert_user_payment_details():
    return httpx.post(user_payment_service_url+"/user/insert_payment_details",json=request.json,headers=Security.get_headers()).json()

@app.route('/get_payment_details_by_id/<string:id>')
def get_payment_details_by_id(id):
    return httpx.get(user_payment_service_url+"/get_payment_details_by_id/"+id,headers=Security.get_headers()).json()

@app.route('/delete_payment_details/<string:id>',methods=['DELETE'])
def delete_payment_details_by_id(id):
    return httpx.delete(user_payment_service_url+"/delete_payment_details/"+id,headers=Security.get_headers()).json()

@app.route('/delete_user_payment_details/<string:user_id>',methods=['DELETE'])
def delete_payment_details_by_userid(user_id):
    return httpx.delete(user_payment_service_url+"/delete_user_payment_details/"+user_id,headers=Security.get_headers()).json()