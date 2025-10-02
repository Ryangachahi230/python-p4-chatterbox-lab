#!/usr/bin/env python3

from random import choice as rc
from faker import Faker
from app import app
from models import db, Message

fake = Faker()

def make_usernames():
    usernames = [fake.first_name() for _ in range(4)]
    if "Duane" not in usernames:
        usernames.append("Duane")
    return usernames

def make_messages():
    # Clear out old messages safely
    Message.query.delete()

    usernames = make_usernames()
    messages = []

    for _ in range(20):
        message = Message(
            body=fake.sentence(),
            username=rc(usernames),
        )
        messages.append(message)

    db.session.add_all(messages)
    db.session.commit()
    print(f"Seeded {len(messages)} messages!")

if __name__ == '__main__':
    with app.app_context():
        make_messages()
