"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User
from api_service import get_all_people, add_people, add_planet, get_all_planets, get_all_users, get_favorites_by_user
# from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace(
        "postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object


@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints


@app.route('/')
def sitemap():
    return generate_sitemap(app)


@app.route('/user', methods=['GET'])
def handle_hello():

    response_body = {
        "msg": "Hello, this is your GET /user response "
    }

    return jsonify(response_body), 200


@app.route('/people', methods=["POST"])
def new_people():
    data = request.get_json()

    name = data.get("name")
    age = data.get("age")
    planet_id = data.get("planet_id")

    if not name or not age or not planet_id:
        return jsonify({"msg": "All the fields are mandatory."}), 400
    
    try:
        person = add_people(name, age, planet_id)
        return jsonify(person), 201

    except Exception as e:
        return jsonify({"msg": str(e)}), 400



@app.route('/people', methods=["GET"])
def get_people():

    try:
        people = get_all_people(None)
        return jsonify(people), 200
    except Exception as e:
        return jsonify({"msg": str(e)})

    
@app.route('/people/<int:id>', methods=["GET"])
def get_people_by_id(id):

    try:
        people = get_all_people(id)
        return jsonify(people), 200
    except Exception as e:
        return jsonify({"msg": str(e)})


@app.route('/planets', methods=["POST"])
def new_planet():
    data = request.get_json()

    name = data.get("name")
    population = data.get("population")
    weather = data.get("weather")

    if not name or not population or not weather:
        return jsonify({"msg": "All the fields are mandatory."}), 400

    try:
        planet = add_planet(name, population, weather)
        return jsonify(planet), 201
    except Exception as e:
        return jsonify({"msg": str(e)}), 400


@app.route('/planets', methods=["GET"])
def get_planets():
    try:
        planets = get_all_planets(None)
        return jsonify({"people": planets}), 200
    except Exception as e:
        return jsonify({"msg": str(e)}), 400


@app.route('/planets/<int:id>', methods=["GET"])
def get_planets_by_id(id):
    try:
        planet = get_all_planets(id)
        return jsonify({"people": planet}), 200
    except Exception as e:
        return jsonify({"msg": str(e)}), 400


@app.route('/users', methods=["GET"])
def get_users():
    try:
        users = get_all_users()
        return jsonify({"users": users}), 200
    except Exception as e:
        return jsonify({"msg": str(e)}), 400
    

@app.route('/users/favorites', methods=["GET"])
def get_user_favorites():
    try:
        favorites = get_favorites_by_user(1)
        return jsonify({"favorites": favorites}), 200
    except Exception as e:
        return jsonify({"msg": str(e)}), 400


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
