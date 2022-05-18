import json
from flask import Flask, jsonify, make_response, request
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
  user_queries = db.ListField()

  def to_json(self): 
    return {
      "user_email": self.user_email,
      "user_name": self.user_name,
      "user_queries": self.user_queries
    }


@app.route('/user/add', methods=["POST"])
def user_add():
  if request.method == "POST":
    data = request.json
    user = users(user_email=data['user_email'], user_name=data['user_name'], user_queries=[])
    user.save()
    return make_response("",201)


@app.route('/user/print', methods=["GET", "POST"])
def user_print():
  if request.method == 'GET':
    pass
    users_list = []
    print(users)
    for user in users.objects:
      users_list.append(user)
    # return str(users_list[0]["id"])
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
    # content = request.json
    # queries = content['user_queries']
    # print(type(queries))
    # print(new_coin)
    db.updateOne({"_id": f"{user_id}"}, {"$push": {"user_queries": new_coin}})
    # print(new_queries)
    # user_obj = users.objects(id=user_id).first()
    # user_obj.update(user_email=content['user_email'], user_name=content['user_name'], user_queries=new_queries)
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
