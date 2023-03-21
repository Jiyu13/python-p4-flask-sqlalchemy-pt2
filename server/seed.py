#!/usr/bin/env python3

from app import app
from models import db, Owner, Pet

import random
from faker import Faker


with app.app_context():
    # 10-1: clear old records
    Pet.query.delete()
    Owner.query.delete()

    # 10-2: create data with faker
    owners = []
    for n in range(20):
        owner = Owner(name=Faker().name())
        owners.append(owner)
    db.session.add_all(owners)

    pets = []
    species = ['Dog', 'Cat', 'Chicken', 'Hamster', 'Turtle']
    for n in range(50):
        pet = Pet(
            name=Faker().name(),
            species=random.choice(species),
            owner=random.choice(owners)
        )
        pets.append(pet)
    db.session.add_all(pets)

    db.session.commit()