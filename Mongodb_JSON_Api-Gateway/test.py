import unittest
import httpx
from settings import *

class MyTestCase(unittest.TestCase):
    user_details = {
        "email": "user@test.com",
        "password": "password",
        "first_name": "user",
        "last_name": "test",
        "phone_number": "0"
    }
    seller_details = {
        "email":"seller@test.com",
        "password":"password",
        "address":{
            "house_address":"test",
            "city":"test",
            "state":"test",
            "country":"test",
            "pincode": 110001
        },
        "no_of_products":0
    }

    user_address = {
        "house_address" : "Howrah",
        "city" : "Kolkata",
        "state" : "West Bengal",
        "country" : "India",
        "postal_code" : 870009 ,
        "mobile" : "0"
    }

    user_payment = {
       "card_number" : "461426447125" ,
       "card_type" : "VISA" ,
       "name_on_card": "user" ,
       "expiry" : "01/26"
    }

    seller_product = {
        "categories": [
            "test"
        ],
        "description": "test product",
        "name": "seller test product",
        "price": 15000,
        "quantity_left": 196,
        "ratings": 8,
        "seller_id": "62fdb012f76721cdb4389346",
        "times_sold": 10004
    }

    coupon = {
        "code" : "test1000" ,
        "min_price" : 1000,
        "max_price" : 30000,
        "discount_price" : 2000
    }

    user_id = ''
    user_token = ''
    seller_id = ''
    seller_token = ''

    user_address_id = ''
    user_payment_id = ''

    seller_product_id = ''

    def test_01_user_register(self):
        response = httpx.post("{}/register/{}".format(server_url,"user"),json=MyTestCase.user_details)
        self.assertEqual(response.status_code,200)
        MyTestCase.user_id = response.json()["_id"]

    def test_02_user_login(self):
        response = httpx.post("{}/login/{}".format(server_url,"user"),json=MyTestCase.user_details)
        self.assertEqual(response.status_code, 200)
        MyTestCase.user_token = response.json()["token"]
        print(MyTestCase.user_token)

    def test_04_seller_register(self):
        response = httpx.post("{}/register/{}".format(server_url, "seller"), json=MyTestCase.seller_details)
        self.assertEqual(response.status_code, 200)
        MyTestCase.seller_id = response.json()["_id"]

    def test_05_seller_login(self):
        response = httpx.post("{}/login/{}".format(server_url, "seller"), json=MyTestCase.seller_details)
        self.assertEqual(response.status_code, 200)
        MyTestCase.seller_token = response.json()["token"]
        print(MyTestCase.seller_token)

    def test_07_user_address_insert(self):
        headers_ = {
            "Authorization" : "Bearer "+MyTestCase.user_token
        }
        response = httpx.post(server_url+"/user/insert_address",json=MyTestCase.user_address,headers=headers_)
        self.assertEqual(response.status_code,200)
        print(response.json())
        self.assertEqual("_id" in response.json(), True)
        MyTestCase.user_address_id = response.json()["_id"]

    def test_08_user_address_count_validation(self):
        headers = {
            "Authorization": "Bearer " + MyTestCase.user_token
        }
        response = httpx.get(server_url+"/user/get_my_addresses",headers=headers)
        self.assertEqual(response.status_code,200)
        self.assertEqual(len(response.json()["addresses"]),1)

    def test_10_user_payment_insert(self):
        headers = {
            "Authorization": "Bearer " + MyTestCase.user_token
        }
        response = httpx.post(server_url + "/user/insert_payment_details", json=MyTestCase.user_payment,
                              headers=headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual("_id" in response.json(), True)
        MyTestCase.user_payment_id = response.json()["_id"]

    def test_11_user_payment_count_validation(self):
        headers = {
            "Authorization": "Bearer " + MyTestCase.user_token
        }
        response = httpx.get(server_url+"/user/get_my_payment_details",headers=headers)
        print(response.json())
        self.assertEqual(response.status_code,200)
        self.assertEqual(len(response.json()["payment_details"]),1)

    def test_13_seller_product_add(self):
        headers = {
            "Authorization": "Bearer " + MyTestCase.seller_token
        }
        response = httpx.post(server_url+"/insert_product",json=MyTestCase.seller_product,headers=headers)
        self.assertEqual(response.status_code,200)
        MyTestCase.seller_product_id = response.json()["_id"]
        print(MyTestCase.seller_product_id)

    def test_14_seller_product_count_validate(self):
        response = httpx.get(server_url+"/get_my_products_id/"+MyTestCase.seller_id)
        self.assertEqual(response.status_code,200)
        self.assertEqual(len(response.json()["product_ids"]),1)
        self.assertEqual(response.json()["product_ids"][0]["_id"],MyTestCase.seller_product_id)
        print(response.json())

    def test_16_coupon_insert(self):
        response = httpx.post(server_url+"/insert_coupon",json=MyTestCase.coupon)
        self.assertEqual(response.status_code,200)

    def test_17_coupon_validation(self):
        response = httpx.get(server_url+"/get_coupons")
        found = False
        for item in response.json()["Coupons"]:
            if item["code"]==MyTestCase.coupon["code"]:
                found = True
                break
        self.assertEqual(found,True)

    def test_19_seller_address(self):
        headers = {
            "Authorization": "Bearer " + MyTestCase.seller_token
        }
        response = httpx.get(server_url+"/seller/get_my_address",headers=headers)
        self.assertEqual(response.status_code,200)
        self.assertEqual(response.json()["address"],MyTestCase.seller_details["address"])

    def test_20_add_to_cart(self):
        headers_ = {
            "Authorization": "Bearer " + MyTestCase.user_token
        }
        response = httpx.post(server_url+"/add_product/"+MyTestCase.seller_product_id,headers=headers_)
        print(response.json())
        self.assertEqual(response.status_code,200)

    def test_21_checkout(self):
        headers_ = {
            "Authorization": "Bearer " + MyTestCase.user_token
        }
        data = {
            "payment_details_id" : MyTestCase.user_payment_id,
            "coupon_code" : MyTestCase.coupon["code"]
        }
        print(MyTestCase.user_payment_id)
        response = httpx.post(server_url+"/checkout",json=data,headers=headers_)
        print(response.json())
        self.assertEqual(response.status_code,200)

    def test_22_orders_validation(self):
        headers_ = {
            "Authorization": "Bearer " + MyTestCase.user_token
        }
        response = httpx.get(server_url+"/get_my_orders",headers=headers_)
        print(response.json())
        self.assertEqual(response.status_code,200)
        self.assertEqual(len(response.json()["Orders"]),1)

    def test_90_user_address_delete(self):
        response = httpx.delete(server_url+"/delete_address/"+MyTestCase.user_address_id)
        self.assertEqual(response.status_code,200)

    def test_91_user_payment_delete(self):
        response = httpx.delete(server_url + "/delete_payment_details/" + MyTestCase.user_payment_id)
        self.assertEqual(response.status_code, 200)

    def test_91_seller_product_delete(self):
        response = httpx.delete(server_url+"/delete_all_products/"+MyTestCase.seller_id)
        self.assertEqual(response.status_code,200)

    def test_92_coupon_delete(self):
        response = httpx.delete(server_url+"/delete_coupon/"+MyTestCase.coupon["code"])
        self.assertEqual(response.status_code,200)

    def test_93_user_delete(self):
        response = httpx.delete("{}/delete_user/{}".format(server_url,MyTestCase.user_id))
        self.assertEqual(response.status_code, 200)

    def test_94_seller_delete(self):
        response = httpx.delete("{}/delete_seller/{}".format(server_url, MyTestCase.seller_id))
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()
