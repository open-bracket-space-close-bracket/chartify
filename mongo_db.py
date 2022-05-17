import mongoengine as db

database_name = "401mid"
DB_URI = f"mongodb+srv://401_mid_group:12345@401cluster.4us9bdk.mongodb.net/{database_name}?retryWrites=true&w=majority"
db.connect(DB_URI)


class Users(db.Document):
  id = db.IntField()
  user_email = db.StringField()
  user_name = db.StringField()
  user_queries = db.StringField()

  def to_json(self): 
    return {
      "id": self.id,
      "user_email": self.user_email,
      "user_name": self.user_name,
      "user_queries": self.user_queries
    }
  
test_user = Users(id=1, user_email="a@gmail.com", user_name="aa", user_queries="a, a")

test_user.save()
db_query = Users.objects(id=1).first()
print(db_query.to_json())
