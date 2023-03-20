#!/usr/bin/env python3

from flask import Flask, make_response
from flask_migrate import Migrate

from models import db, Pet, Owner

app = Flask(__name__)
# configuration to connect app to the db
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'

# disable track modifications
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# configure the app and models for Flask-Migrate
migrate = Migrate(app, db)

# connects db to app before ir runs
db.init_app(app)