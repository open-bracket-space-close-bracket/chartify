import json
from flask import Flask, jsonify, make_response, request
import requests
from flask_mongoengine import MongoEngine

app = Flask(__name__)

database_name = "401Mid"
DB_URI = f"mongodb+srv://DJLMT:12345@quickstartusers.zmxlh.mongodb.net/{database_name}?retryWrites=true&w=majority"
app.config["MONGODB_HOST"] = DB_URI


db = MongoEngine()
db.database_name = database_name
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


## figure out how to get a user's _ID on mongo as they're added
## figure out how to get a user's _ID on mongo once they log in (assuming they already have a mongoDB _ID)


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

@app.route('/users/ids')
def do_things():
  if request.method == "GET":
    data = request.json
    try:
      user = compare_and_find(data["user_email"])
    except:
      url = "http://127.0.0.1:5000/user/add"
      data = {"user_email": data["user_email"], "user_name": data['user_name']}
      requests.post(url, json= data)
      response = requests.get("http://127.0.0.1:5000/users/ids", json=data)
      return response._content
    return str(user)

@app.route('/user/add', methods=["POST"])
def user_add():
  if request.method == "POST":
    data = request.json
    user = users(user_email=data['user_email'], user_name=data['user_name'], user_queries="")
    user.save()
    return make_response("",201)


@app.route('/user/print', methods=["GET", "POST"])
def user_print():
  if request.method == 'GET':
    users_list = []
    for user in users.objects:
      users_list.append(user)
    return make_response(jsonify(users_list),200)
  elif request.method == "POST":
    content = request.json
    user = users(user_email=content["user_email"],user_name=content['user_name'],user_queries=content["user_queries"],)
    user.save()
    return make_response("", 201)

@app.route('/user/print/<user_id>/<new_coin>', methods=["GET","PUT","DELETE"])
def each_user_functions(user_id, new_coin):
  if request.method == "GET":
    user_obj = users.objects(id=user_id).first()
    if user_obj:
      return make_response(jsonify(user_obj.to_json()),200)
    else:
      return make_response("", 404)
  elif request.method == "PUT":
    content = request.json
    queries = content['user_queries']
    if queries == "": 
      new_queries = queries + new_coin
    # print(type(queries))
    # print(new_coin)
    else: 
      new_queries = queries + f", {new_coin}"
    user_obj = users.objects(id=user_id).first()
    user_obj.update(user_email=content['user_email'], user_name=content['user_name'], user_queries=new_queries)
    return make_response('', 204)
  elif request.method == "DELETE":
    user_obj = users.objects(id=user_id).first()
    user_obj.delete()
    return make_response("", 410)


if __name__=="__main__":
  app.run()

# db.connect(host=DB_URI)



  



# db_query = Users.objects(id=1).first()
# print(db_query.to_json())
