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


# 1. put the data onto internet
@app.route('/')
def index():
    # make_response() accepts the same args that can be returned from a view function, 
    # create a response obj with a 200 statu code
    response = make_response(
        '<h1>Welcome to the pet/owner directory!</h1>',
        200
    )
    # return response obj to the client after a request
    return response


# 2. show pet data in Flask app on browser
@app.route('/pets/<int:id>')
def pet_by_id(id):
    pet = Pet.query.filter(Pet.id == id).first()

    # 3. set condition
    if not pet:
        response_body = "<h1>404 pet not found</h1>"
        response = make_response(response_body, 404)
        return response

    response_body = f'''
        <h1>Information for {pet.name}</h1>
        <h2>Pet Species is {pet.species}</h2>
        <h2>Pet Owner is {pet.owner.name}</h2>
    '''

    response = make_response(response_body, 200)
    return response


# 4. filter owner by id and show his/her pets if has any
@app.route('/owner/<int:id>')
def owner_by_id(id):
    owner = Owner.query.filter(Owner.id == id).first()

    if not owner:
        response_body = f"<h1>404 owner not found"
        response = make_response(response_body, 404)
        return response
    
    response_body = f"<h1>Information for {owner.name}</h1>"

    pets = [pet for pet in owner.pets]
    if not pets:
        response_body += f"<h2>Has no pets at this time</h2>"

    else:
        for pet in pets:
            response_body += f'''<h2>Has pet {pet.species} named {pet.name}</h2>'''
    
    response = make_response(response_body, 200)
    return response


if __name__ == '__main__':
    app.run(port=5555, debug=True)
