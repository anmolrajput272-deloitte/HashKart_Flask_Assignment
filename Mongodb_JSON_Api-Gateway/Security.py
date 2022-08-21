from flask import request, jsonify
import jwt
from functools import wraps
from settings import secret_key

def seller_token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token or len(token)<8:
            return jsonify({'message':'Token is missing'}), 400
        token = token[7:]
        try:
            decoded_jwt = jwt.decode(token,secret_key)
            if(decoded_jwt['user_type']=="user"):
                return jsonify({"message":"You are not allowed to access user panel"}), 400
        except:
            return jsonify({'message':'JSON Invalid'}), 400
        return f(*args,**kwargs)
    return decorated

def user_token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token or len(token)<8:
            return jsonify({'message':'Token is missing'})
        token = token[7:]
        try:
            decoded_jwt = jwt.decode(token,secret_key)
            if (decoded_jwt['user_type'] == "seller"):
                return jsonify({"message": "You are not allowed to access seller panel"})
        except:
            return jsonify({'message':'JSON Invalid'})
        return f(*args,**kwargs)
    return decorated


def auth():
    return jsonify({"message":"Authentication Successful"}) , 200

def get_headers():
    headers_ = {}
    if "Authorization" in request.headers:
        headers_["Authorization"] = request.headers.get('Authorization')
    return headers_
