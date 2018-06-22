from modules.twitter_user import TwitterUser
import json
from app.models import Actor
from app import db
from unidecode import unidecode

# Adding actors from helpers/politicians.json
print("Adding Actors")
actors = json.load(open("helpers/politicians.json"))
for row in actors:
    username = row["twitter_handle"]
    user = TwitterUser(username)
    if user.existence == True:
        name = user.name
        name = unidecode(name)
        if not Actor.query.filter_by(id=user.id).first():
            f = Actor(id = int(user.id), username=username, name= name)
            db.session.add(f)
            db.session.commit()
            print(name, "added")






