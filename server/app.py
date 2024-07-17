from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate
from flask_restful import Resource, Api
from models import db, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)
api = Api(app)
db.init_app(app)
class MessagesResource(Resource):
    def get(self):
        messages = [message.to_dict() for message in Message.query.all()]
        return messages, 200
    def post(self):
        data = request.get_json()
        body = data.get("body")
        username = data.get("username")
        message = Message(body=body, username=username)
        db.session.add(message)
        db.session.commit()
        return message.to_dict(), 201


api.add_resource(MessagesResource, "/messages", endpoint="messages")


class MessageResource(Resource):
    def patch(self,id):
        message = Message.query.get(id)
        data = request.get_json()
        for key, value in data.items():
            setattr(message, key, value)
        db.session.add(message)
        db.session.commit()
        return message.to_dict(), 200

    def delete(self,id):
        message = Message.query.get(id)
        db.session.delete(message)
        db.session.commit()
        return {}, 204
    
api.add_resource(MessageResource, "/messages/<int:id>", endpoint="message")


if __name__ == '__main__':
    app.run(port=5555)
