import jwt
from settings import secret_key

def get_id_from_jwt(token):
    return jwt.decode(token[7:], secret_key)['_id']