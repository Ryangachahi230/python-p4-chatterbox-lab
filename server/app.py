from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_migrate import Migrate
from models import db, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)  # allow React frontend
db.init_app(app)
migrate = Migrate(app, db)

# GET all messages
@app.route('/messages', methods=['GET'])
def get_messages():
    messages = Message.query.order_by(Message.created_at.asc()).all()
    return jsonify([m.to_dict() for m in messages]), 200

# POST a new message
@app.route('/messages', methods=['POST'])
def create_message():
    data = request.get_json() or {}
    body = data.get("body", "").strip()
    username = data.get("username", "").strip()

    if not body or not username:
        return jsonify({"error": "Both 'body' and 'username' are required."}), 400

    message = Message(body=body, username=username)
    db.session.add(message)
    db.session.commit()
    return jsonify(message.to_dict()), 201

# PATCH an existing message
@app.route('/messages/<int:id>', methods=['PATCH'])
def update_message(id):
    message = db.session.get(Message, id)  # modern SQLAlchemy
    if not message:
        return jsonify({"error": "Message not found."}), 404

    data = request.get_json() or {}
    body = data.get("body", "").strip()

    if not body:
        return jsonify({"error": "'body' is required and cannot be empty."}), 400

    message.body = body
    db.session.commit()
    return jsonify(message.to_dict()), 200

# DELETE a message
@app.route('/messages/<int:id>', methods=['DELETE'])
def delete_message(id):
    message = db.session.get(Message, id)
    if not message:
        return jsonify({"error": "Message not found."}), 404

    db.session.delete(message)
    db.session.commit()
    return jsonify({"message": f"Message {id} deleted."}), 200  # consistent JSON
    # OR keep `204` if your React handles it cleanly

if __name__ == '__main__':
    app.run(port=5555, debug=True)
