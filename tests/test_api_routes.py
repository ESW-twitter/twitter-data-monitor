from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
import os

from app import app

class TestAPIRoutes():

    def setUp():
        print("Rodando setup...\n")
        app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite://"
        app.config['TESTING'] = True
        db.create_all()

    def tearDown():
        print("Rodando tear down...\n")
        db.drop_all()


    def test(self):
        TestAPIRoutes.setUp()
