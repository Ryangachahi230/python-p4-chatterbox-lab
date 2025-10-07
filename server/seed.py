from app import app
from models import db, Message

with app.app_context():
    print("Seeding database...")

    Message.query.delete()

    m1 = Message(body="Hello, World!", username="Ian")
    m2 = Message(body="Flask + React = ❤️", username="Ryan")

    db.session.add_all([m1, m2])
    db.session.commit()

    print("Seeding complete!")
