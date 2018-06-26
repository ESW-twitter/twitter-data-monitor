from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import json
from flask import jsonify
import os

from app import app,db
from app.api_routes import *
from app.models import Actor,TweetReport,RelationReport
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
        user = TwitterUser('CNN')
        user = Actor(user.id, user.username, user.name)

        with app.app_context():
            TestAPIRoutes.setUp()
            db.session.add(user)
            db.session.commit()
            response = api_get_actors()
            TestAPIRoutes.tearDown()

        assert '{"actors":["CNN"],"code":"200","length":1,"message":"Success"}\n' == response.get_data().decode()


    def test_api_actors_datetime(self):
        a = ActorReport('01/02/2018', None, None)
        b = ActorReport('02/02/2018', None, None)
        c = ActorReport('02/02/2018', None, None)

        with app.app_context():
            TestAPIRoutes.setUp()
            db.session.add(a)
            db.session.add(b)
            db.session.add(c)
            db.session.commit()
            response = api_get_actors_datetime()
            TestAPIRoutes.tearDown()

        assert '{"code":"200","dates":["01/02/2018","02/02/2018"],"message":"Success"}\n' or '{"code":"200","dates":["02/02/2018","01/02/2018"],"message":"Success"}\n' == response.get_data().decode()

    def test_api_get_actor_account_date_invalid_user(self):

        with app.app_context():
            TestAPIRoutes.setUp()
            response = api_get_actor_account_date('CNN', None)
            TestAPIRoutes.tearDown()

        assert '400' == json.loads(response.get_data().decode())['code']

    def test_api_get_actor_account_date_none_date(self):
        user = TwitterUser('Renova_BR')
        user = Actor(user.id, user.username, user.name)
        with app.app_context():
            TestAPIRoutes.setUp()
            db.session.add(user)
            db.session.commit()
            response = api_get_actor_account_date('Renova_BR', None)
            TestAPIRoutes.tearDown()
        assert '200' == json.loads(response.get_data().decode())['code']

    def test_api_get_actor_account_date_zero_reports(self):
        user = TwitterUser('Renova_BR')
        user = Actor(user.id, user.username, user.name)
        with app.app_context():
            TestAPIRoutes.setUp()
            db.session.add(user)
            db.session.commit()
            response = api_get_actor_account_date('Renova_BR', '01-01-2018')
            TestAPIRoutes.tearDown()
        assert '500' == json.loads(response.get_data().decode())['code']


    def test_api_get_actor_account_date(self):
        csv_content = 'nome;seguidores;tweets;seguindo;curtidas;retweets;favorites;hashtags;mentions\n923257662569148417;1715;146;193;104;0;0;;;\n'
        a = ActorReport('01-01-2018', '12:00', csv_content.encode())
        user = TwitterUser('Renova_BR')
        user = Actor(user.id, user.username, user.name)
        with app.app_context():
            TestAPIRoutes.setUp()
            db.session.add(a)
            db.session.add(user)
            db.session.commit()
            response = api_get_actor_account_date('Renova_BR', '01-01-2018')
            TestAPIRoutes.tearDown()

        assert '{"12:00":{"date":"01-01-2018","followers_count":"193","following_count":"104","likes_count":"0","name":"1715","tweets_count":"0","username":"146"},"code":"200","message":["Success"]}\n' == response.get_data().decode()

    def test_api_get_actor_account_date_tweets(self):
        csv_content = 'Data;Texto;Autor(RT);Retweets;Curtidas;Hashtags;Mentions\n2018-06-08 14:25:30;@MarcioQuessada Pressionar e discutir. Essa mudanca dificilmente vai vir deles!;;0;0; ;MarcioQuessada;'
        user = TwitterUser('Renova_BR')
        user = Actor(user.id, user.username, user.name)
        t = TweetReport('12-06-2018', '19:00',user.id, csv_content.encode())
        with app.app_context():
            TestAPIRoutes.setUp()
            db.session.add(t)
            db.session.add(user)
            db.session.commit()
            response = api_get_actor_account_date_tweets('Renova_BR', '12-06-2018')
            TestAPIRoutes.tearDown()
        assert '{"code":"200","message":"Success","tweets":[{"date":"2018-06-08 14:25:30","hashtags":" ","likes":"0","mention":"MarcioQuessada","retweets":"0","rt_author":"","text":"@MarcioQuessada Pressionar e discutir. Essa mudanca dificilmente vai vir deles!"}]}\n'== response.get_data().decode()

    def test_api_get_relations_zero_reports(self):
        with app.app_context():
            TestAPIRoutes.setUp()
            response = api_get_relations()
            TestAPIRoutes.tearDown()
        assert '{"code":"400","details":"Sorry, no information was found.","message":"Bad Request"}\n' == response.get_data().decode()

    def test_api_get_relations(self):
        csv_content = 'Retweeta;Retweetado;Numero\nfrentebrasilpop;LulapeloBrasil;19\n'
        relation  = RelationReport('12-06-2018','19:00',csv_content.encode())
        with app.app_context():
            TestAPIRoutes.setUp()
            db.session.add(relation)
            db.session.commit()
            response = api_get_relations()
            TestAPIRoutes.tearDown()
        assert '{"code":"200","dates":["12-06-2018"],"message":"Success"}\n' == response.get_data().decode()

    def test_api_get_relations_actor_zero_reports(self):
        with app.app_context():
            TestAPIRoutes.setUp()
            db.session.commit()
            response = api_get_relations_actor('12-06-2018')
            TestAPIRoutes.tearDown()
        assert '{"code":"400","details":"Sorry, no information was found.","message":"Bad Request"}\n' == response.get_data().decode()

    def test_api_get_relations_actor(self):
        csv_content = 'Retweeta;Retweetado;Numero\nfrentebrasilpop;LulapeloBrasil;19\nfrentebrasilpop;MST_Oficial;14\n'
        csv_content2 = 'Retweeta;Retweetado;Numero\nPOVOsemMEDO;MST_Oficial;98\nPOVOsemMEDO;cirogomes;1\nPOVOsemMEDO;mtst;3\n'
        relation  = RelationReport('12-06-2018','19:00',csv_content.encode())
        relation2 = RelationReport('05-06-2018','15:00',csv_content2.encode())
        with app.app_context():
            TestAPIRoutes.setUp()
            db.session.add(relation)
            db.session.add(relation2)
            db.session.commit()
            response = api_get_relations_actor('12-06-2018')
            TestAPIRoutes.tearDown()
        assert '{"19:00":{"frentebrasilpop":[{"LulapeloBrasil":"19"},{"MST_Oficial":"14"}]},"code":"200","message":"Success"}\n' == response.get_data().decode()
