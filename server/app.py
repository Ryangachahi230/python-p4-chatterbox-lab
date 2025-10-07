from flask import Flask, request, jsonify
from flask_migrate import Migrate
from flask_cors import CORS
from models import db, Message

app = Flask(__name__)
CORS(app)

# Configure the database
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)
migrate = Migrate(app, db)


# -------------------- ROUTES -------------------- #

@app.route("/messages", methods=["GET", "POST"])
def messages():
    if request.method == "GET":
        messages = Message.query.order_by(Message.created_at.asc()).all()
        return jsonify([m.to_dict() for m in messages]), 200

    elif request.method == "POST":
        data = request.get_json()

        if not data.get("body") or not data.get("username"):
            return jsonify({"error": "Missing required fields"}), 400

        new_message = Message(
            body=data.get("body"),
            username=data.get("username")
        )

        db.session.add(new_message)
        db.session.commit()

        return jsonify(new_message.to_dict()), 201


@app.route("/messages/<int:id>", methods=["PATCH", "DELETE"])
def message_by_id(id):
    message = Message.query.get(id)

    if not message:
        return jsonify({"error": "Message not found"}), 404

    if request.method == "PATCH":
        data = request.get_json()
        if "body" in data:
            message.body = data["body"]
        db.session.commit()
        return jsonify(message.to_dict()), 200

    elif request.method == "DELETE":
        db.session.delete(message)
        db.session.commit()
        return "", 204


if __name__ == "__main__":
    app.run(port=5555, debug=True)
