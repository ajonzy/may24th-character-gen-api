from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS
from flask_heroku import Heroku

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgres://pxfqvqnlhhgplc:4e5ccfe9920bc3ab750189bf8b79687dec8397563564f89b8ca26365e5aecafd@ec2-3-216-129-140.compute-1.amazonaws.com:5432/dd3uke32t9u59m"

db = SQLAlchemy(app)
ma = Marshmallow(app)

heroku = Heroku(app)
CORS(app)


class Character(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    character_class = db.Column(db.String(), nullable=False)
    hitpoints = db.Column(db.Integer, nullable=False)

    def __init__(self, name, character_class):
        self.character_class = character_class,
        self.hitpoints = 100
        self.name = name

class CharacterSchema(ma.Schema):
    class Meta:
        fields = ("id", "name", "character_class", "hitpoints")

character_schema = CharacterSchema()
characters_schema = CharacterSchema(many=True)


@app.route("/character/add", methods=["POST"])
def add_character():
    if request.content_type != "application/json":
        return jsonify("Error: Data must be sent as JSON")

    post_data = request.get_json()
    name = post_data.get("name")
    character_class = post_data.get("character_class")

    record = Character(name, character_class)
    db.session.add(record)
    db.session.commit()

    return jsonify("Character Created")

@app.route("/character/get", methods=["GET"])
def get_all_characters():
    all_characters = db.session.query(Character).all()
    return jsonify(characters_schema.dump(all_characters))

@app.route("/character/get/<id>", methods=["GET"])
def get_character_by_id(id):
    character = db.session.query(Character).filter(Character.id == id).first()
    return jsonify(character_schema.dump(character))

@app.route("/character/delete/<id>", methods=["DELETE"])
def delete_character_by_id(id):
    character = db.session.query(Character).filter(Character.id == id).first()
    db.session.delete(character)
    db.session.commit()
    return jsonify("Character Deleted")


if __name__ == "__main__":
    app.run(debug=True)