from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
import json
from flask import jsonify
import os

from app import app,db
from app.api_routes import *
from app.models import Actor
from modules.twitter_user import TwitterUser

app = Flask(__name__)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
db.init_app(app)
# client = app.test_client()

class TestAPIRoutes():

    def setUp():
        print("Rodando setup...\n")
        with app.app_context():
            db.create_all()

    def tearDown():
        print("Rodando tear down...\n")
        db.drop_all()


    def test_api_get_actors(self):
        TestAPIRoutes.setUp()
        user = TwitterUser('CNN')
        user = Actor(user.id, user.username, user.name)

        with app.app_context():
            db.session.add(user)
            db.session.commit()
            response = api_get_actors()

        assert '{"actors":["CNN"],"code":"200","length":1,"message":"Success"}\n' == response.get_data().decode()

        TestAPIRoutes.tearDown()

    def test_api_actors_datetime(self):
        TestAPIRoutes.setUp()

        a = ActorReport('01/02/2018', None, None)
        b = ActorReport('02/02/2018', None, None)
        c = ActorReport('03/02/2018', None, None)

        with app.app_context():
            db.session.add(a)
            db.session.add(b)
            db.session.add(c)
            db.session.commit()
            response = api_get_actors_datetime()

        assert '{"code":"200","dates":["01/02/2018","02/02/2018","03/02/2018"],"message":"Success"}\n' == response.get_data().decode()
        TestAPIRoutes.tearDown()

    def test_api_get_actor_account_date(self):
        TestAPIRoutes.setUp()
