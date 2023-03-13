#!/usr/bin/env python3

from random import choice as rc
from faker import Faker
from app import app
from models import db, Owner, Pet

#  1. initialize the application with our SQLAlchemy instance to connect db and app
# db.init_app(app)
fake = Faker()

# 2. create app_context() to ensure that apps fail quickly if they aren't configured with this context
with app.app_context():
    # 3. clear our tables in db through models
    Pet.query.delete()
    Owner.query.delete()

    # make a list to store all owner instance
    owners = []
    # generate attributes with random and faker
    for n in range(50):
        owner = Owner(name=fake.name())
        owners.append(owner)
    
    db.session.add_all(owners)

    # make a list to store all pet instance
    pets = []
    species = ["Dog", "Cat", "Chicken", "Hamster", "Turtle"]
    for n in range(100):
        pet = Pet(name=fake.first_name(), species=rc(species), owner=rc(owners))
        pets.append(pet)

    db.session.add_all(pets)
    # commit the transaction
    db.session.commit()