import json
from flask import Flask, jsonify, make_response, request
import requests
from flask_mongoengine import MongoEngine
import os

app = Flask(__name__)

DB_URI = os.environ.get("DB_URI",None)
app.config["MONGODB_HOST"] = DB_URI


db = MongoEngine()
# db.database_name = database_name
db.init_app(app)

class users(db.Document):
  user_email = db.StringField()
  user_name = db.StringField()
  user_queries = db.StringField()

  def to_json(self): 
    return {
      "user_email": self.user_email,
      "user_name": self.user_name,
      "user_queries": self.user_queries
    }

def get_all_ids(): 
  users_dict = {}
  for user in users.objects:
    user_email = user["user_email"]
    users_dict[f"{user_email}"] = user["id"]
  return users_dict

def compare_and_find(user_email=None):
  ids = get_all_ids()
  user = ids[user_email]
  return user


def do_things(request):
  if request.method == "GET":
    data = request.json
    try:
      user = compare_and_find(data["user_email"])
    except:
      url = "https://djlmt-chartify.herokuapp.com/user/add"
      data = {"user_email": data["user_email"], "user_name": data['user_name']}
      requests.post(url, json= data)
      response = requests.get("https://djlmt-chartify.herokuapp.com/users/ids", json=data)
      return response._content
    return str(user)


def user_add(request):
  if request.method == "POST":
    data = request.json
    user = users(user_email=data['user_email'], user_name=data['user_name'], user_queries="")
    user.save()
    return make_response("",201)



def user_print(request, user_id):
  if request.method == "GET":
    user_obj = users.objects(id=user_id).first()
    if user_obj:
      return make_response(jsonify(user_obj.to_json()),200)
    else:
      return make_response("", 404)
  # elif request.method == "POST":
  #   content = request.json
  #   user = users(user_email=content["user_email"],user_name=content['user_name'],user_queries=content["user_queries"],)
  #   user.save()
  #   return make_response("", 201)


def each_user_functions(user_id, new_coin, request):
  if request.method == "PUT":
    content = request.json
    queries = content['user_queries']
    if queries == "": 
      new_queries = queries + new_coin
    else: 
      new_queries = queries + f", {new_coin}"
    user_obj = users.objects(id=user_id).first()
    user_obj.update(user_email=content['user_email'], user_name=content['user_name'], user_queries=new_queries)
    return make_response('', 204)

  # REWORK -- To get it to delete from the user_queries rather than the entire Entry.
  elif request.method == "DELETE":
    user_obj = users.objects(id=user_id).first()
    user_obj.delete()
    return make_response("", 410)


if __name__=="__main__":
  app.run()
