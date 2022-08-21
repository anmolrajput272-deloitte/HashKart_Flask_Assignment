from Config import app
import user_service
import cart_service
import coupon_service
import order_service
import product_service
import seller_address_service
import user_address_service
import user_payment_service
from flask import send_from_directory
from flask_swagger_ui import get_swaggerui_blueprint

@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static',path)

SWAGGER_URL = '/swagger'
API_URL = '/static/swagger.json'
SWAGGERUI_BLUEPRINT = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Seans-Python-Flask-REST-Boilerplate"
    }
)

app.register_blueprint(SWAGGERUI_BLUEPRINT, url_prefix=SWAGGER_URL)

app.run(port=5000)
