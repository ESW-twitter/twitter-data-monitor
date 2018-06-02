from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from app import app
from app import models
import os


def setUp():
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite://"
    app.config['TESTING'] = True
    db.create_all()

def tearDown():
    db.drop_all()
