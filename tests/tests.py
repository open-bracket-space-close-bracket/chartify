import requests
import json
import random

url= "http://127.0.0.1:5000"

def test_get_id():
  id_url = url + "/users/ids"
  data = {"user_email": "brooksjamesk01@gmail.com", "user_name": "James"}
  response = requests.get(id_url, json=data)
  user_id = response.text
  assert user_id == "6287d390c1ec47738f0178c1"

def test_known_user_queries():
  query_url = url + "/user/print/6287d390c1ec47738f0178c1"
  response = requests.get(query_url)
  json_obj = json.loads(response.text)
  user_queries = json_obj["user_queries"]
  list_format = user_queries.split(", ")
  assert list_format[0] == "BTC"

def test_post_user():
  post_url = url + "/user/add"
  rand_number = random.randint(1,300)
  user_name = f"Pytestington the III{rand_number}"
  data = {"user_email": "pytest@gmail.com", "user_name": user_name}
  response = requests.post(post_url, json=data)
  assert response.status_code == 200

def test_coin_route_baseball():
  coin_url = url + "/api/baseball"
  response = requests.get(coin_url)
  assert response.status_code == 200
