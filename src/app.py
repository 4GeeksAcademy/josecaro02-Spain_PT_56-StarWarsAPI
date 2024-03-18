"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
cambios en app
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Planets, Favorite_Planets
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
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

@app.route('/users', methods=['GET'])
def handle_hello():
    #SELECT * FROM user;
    users = User.query.all()
    
    #users_serialized_map = list(map(lambda x: x.serialize(), users))

    users_serialized = []
    for user in users:
        users_serialized.append(user.serialize())

    response_body = {
        "msg": "ok",
        "result": users_serialized
    }

    return jsonify(response_body), 200

@app.route('/planets', methods=['GET'])
def get_planets():
    planets = Planets.query.all()
    print(planets)
    planets_serialized=[]
    for x in planets:
        planets_serialized.append(x.serialize())
    return jsonify({"msg": "ok", "results": planets_serialized}), 200

@app.route('/planets/<int:id>', methods=['GET'])
def get_single_planet(id):
    planet = Planets.query.get(id)
    print(planet)
    return jsonify({"msg": "ok", "planet": planet.serialize()})

@app.route('/planets', methods=['POST'])
def add_planet():
    body = request.get_json(silent=True)
    if body is None:
        return jsonify("Debes enviar información en el body"), 400
    if 'name' not in body:
        return jsonify("El campo name es obligatorio"), 400
    new_planet = Planets()
    new_planet.name = body['name']
    db.session.add(new_planet)
    db.session.commit()
    return jsonify("Planeta agregado satisfactoriamente"), 200

#body -> user_id
@app.route('/user/favorites', methods=['GET'])
def favorites_user():
    body = request.get_json(silent=True)
    if body is None:
        return jsonify({'msg': 'Debes enviar información en el body'}), 400
    if 'user_id' not in body:
        return jsonify({'msg': 'El campo user_id es obligatorio'}), 400
    user = User.query.get(body['user_id'])
    if user is None:
        return jsonify({'msg': "El usuario con el id: {} no existe".format(body['user_id'])}), 404
    favorite_planets = db.session.query(Favorite_Planets, Planets).join(Planets).filter(Favorite_Planets.user_id == body['user_id']).all()
    print(favorite_planets)
    favorite_planets_serialized = []
    for favorite_item, planet_item in favorite_planets:
        #id en favorite planets, información del planeta
        favorite_planets_serialized.append({'favorite_planet_id': favorite_item.id, 'planet': planet_item.serialize()})

    return jsonify({'msg':'ok', 'results': favorite_planets_serialized})

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
