#!/usr/bin/env python3

from flask import Flask, make_response, request, jsonify
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


@app.route('/')
def index():
    return make_response(
        '<h1>Welcome to the pet/owner directory!</h1>',
        200
    )


@app.route('/owners', methods=['GET'])
def owners():
    if request.method == "GET":
        owners = Owner.query.all()
        
        owners_dict = []
        for owner in owners:
            # make query obj into a dictionary
            owner_dict = {
                "name": owner.name
            }
            owners_dict.append(owner_dict)
        return make_response(jsonify(owners_dict), 200)


@app.route('/owners/<int:id>')
def owner_by_id(id):
    owner = Owner.query.filter_by(id=id).first()
    if not owner:
        response_body = {"message": "This owner doesn't exist."}
        return make_response(response_body, 404)
    
    else:
        pets = owner.pets
        if not pets:
            response_body = {"message": "This owner doesn't have pets."}
            return make_response(response_body, 404)

        pets_dict_list = []
        for pet in pets:
            pet_dict = {
                "name": pet.name,
                "species": pet.species,
                "owner_id": pet.owner_id
            }
            pets_dict_list.append(pet_dict)
        owner_dict = {
            "name": owner.name,
            "pets": pets_dict_list
        }
        return make_response(owner_dict, 200)


@app.route('/pets', methods=['GET'])
def pets():
    if request.method == "GET":
        pets = Pet.query.all()
        
        pets_dict = []
        for pet in pets:
            # make query obj into a dictionary
            pet_dict = {
                "name": pet.name,
                "species": pet.species,
                "owner_id": pet.owner_id
            }
            pets_dict.append(pet_dict)
        return make_response(jsonify(pets_dict), 200)


@app.route('/pets/<int:id>')
def pet_by_id(id):
    pet = Pet.query.filter_by(id=id).first()
    if not pet:
        response  = {
            "message": "Pet does not exit."
        }
        return make_response(response, 404)
    pet_dict = {
        "name": pet.name,
        "species": pet.species,
        "owner_id": pet.owner_id
    }
    return make_response(pet_dict, 200)


if __name__ == "__main__":
    app.run(port=5555, debug=True)