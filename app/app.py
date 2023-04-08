from flask import Flask, jsonify, json, request
from datetime import date, datetime
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from sqlalchemy import true
from datetime import datetime, timedelta, timezone,date
from pytz import timezone as tz
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
# from schemas import CargoSchema, SpaceshipSchema, CaptainSchema

app = Flask(__name__)
CORS(app, supports_credentials=True)

# database configuration settings
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://admin:Nirmilapk412!@spacedb.cikkevvaa4w7.us-east-2.rds.amazonaws.com:3306/spacedb'
app.config['SECRET_KEY'] = 'secret-key-goes-here'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

migrate = Migrate()
migrate.init_app(app, db)


class Cargo(db.Model):
    """Cargo model to store cargo details"""
    __tablename__ = 'cargo'
    id = db.Column(db.Integer, primary_key=True)
    weight = db.Column(db.Float)
    cargotype = db.Column(db.String(50))
    departure = db.Column(db.Date)
    arrival = db.Column(db.Date)
    shipid = db.Column(db.Integer, db.ForeignKey('spaceship.id'))

class CargoSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Cargo

class Spaceship(db.Model):
    """Spaceship model to store spaceship details"""
    __tablename__ = 'spaceship'
    id = db.Column(db.Integer, primary_key=True)
    maxweight = db.Column(db.Float)
    captainid = db.Column(db.Integer, db.ForeignKey('captain.id'))

class SpaceshipSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Spaceship


class Captain(db.Model):
    """Captain model to store captain details"""
    __tablename__ = 'captain'
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(50))
    lastname = db.Column(db.String(50))
    rank = db.Column(db.String(50))
    homeplanet = db.Column(db.String(50))

class CaptainSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Captain

# Pre-configured username and password
USERNAME = 'admin'
PASSWORD = 'password'

# User login endpoint
@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    # Check if username and password are provided
    if not username or not password:
        return jsonify({'message': 'Username and password are required'}), 400

    # Check if user exists and if password is correct
    if username == USERNAME and password == PASSWORD:
        # Get all the current cargo that's being transported and hasn't arrived yet
        completed = request.args.get('completed', False)
        # check for toggle complete
        if completed:
            cargo = Cargo.query.filter(Cargo.arrival.isnot(None)).all()
        else:
            cargo = Cargo.query.filter(Cargo.arrival.is_(None)).all()

        cargo_schema = CargoSchema(many=True)
        result = cargo_schema.dump(cargo)

        # Return the message and current cargo data to the user
        return jsonify({'message': 'Login successful!', 'cargo': result}), 200
    else:
        return jsonify({'message': 'Invalid username or password.'}), 401


# cargo endpoint to get all cargo
@app.route("/api/cargo" , methods = ['GET'])
def get_all_cargo():
    cargo = Cargo.query.all()
    result = CargoSchema().dump(cargo, many=True)
    return jsonify(result)

# Cargo endpoint to one cargo
@app.route('/api/cargo/<int:id>', methods=['GET'])
def get_cargo(id):
    cargo = Cargo.query.get(id)
    if cargo:
        result = CargoSchema().dump(cargo)
        return jsonify(result)
    return jsonify({'message': 'Cargo not found'}), 404

# cargo endpoint for creating & storing new cargo
@app.route('/api/cargo', methods=['POST'])
def add_cargo():
    data = request.get_json()
    cargo = Cargo(
        weight=data['weight'],
        cargotype=data['cargotype'],
        departure=data['departure'],
        shipid=data['shipid']
    )
    db.session.add(cargo)
    db.session.commit()
    return jsonify(CargoSchema().dump(cargo))

# cargo endpoint for updating new cargo
@app.route('/api/cargo/<int:id>', methods=['PUT'])
def update_cargo(id):
    data = request.get_json()
    cargo = Cargo.query.get(id)
    if cargo:
        cargo.weight = data.get('weight', cargo.weight)
        cargo.cargotype = data.get('cargotype', cargo.cargotype)
        cargo.departure = data.get('departure', cargo.departure)
        cargo.arrival = data.get('departure', cargo.arrival)
        cargo.shipid = data.get('shipid', cargo.shipid)

        # Check if there is enough room on the selected ship for the cargo
        ship = Spaceship.query.get(cargo.shipid)
        if not ship or ship.maxweight < cargo.weight:
            return {'error': 'Selected spaceship does not exist or does not have enough room for the cargo.'}, 400

        # Update departure and arrival if they are provided
        if 'departure' in data:
            cargo.departure = data['departure']
        if 'arrival' in data:
            cargo.arrival = data['arrival']

        # save cargo to database
        db.session.commit()
        return CargoSchema.dump(cargo)
    return {'error': 'Cargo not found.'}, 404

# cargo endpoint to delete cargo entries
@app.route('/api/cargo/<int:id>', methods=['DELETE'])
def delete_cargo(id):
    cargo = Cargo.query.get(id)
    if cargo:
        db.session.delete(cargo)
        db.session.commit()
        return jsonify({'message': 'Cargo deleted successfully'})
    return jsonify({'message': 'Cargo not found'}), 404

# spaceship endpoints
# Spaceship endpoint to get all spaceships
@app.route('/api/spaceships', methods=['GET'])
def get_all_spaceships():
    spaceships = Spaceship.query.all()
    result = SpaceshipSchema().dump(spaceships, many=True)
    return jsonify(result)

# Spaceship endpoint to one spaceship
@app.route('/api/spaceship/<int:id>', methods=['GET'])
def get_spaceship(id):
    spaceship = Spaceship.query.get(id)
    if spaceship:
        result = SpaceshipSchema().dump(spaceship)
        return jsonify(result)
    return jsonify({'message': 'Spaceship not found'}), 404

# Spaceship endpoint to create and store a spaceship
@app.route('/api/spaceship', methods=['POST'])
def add_spaceship():
    data = request.get_json()
    spaceship = SpaceshipSchema().load(data)
    db.session.add(spaceship)
    db.session.commit()
    result = SpaceshipSchema().dump(spaceship)
    return jsonify(result)

# Spaceship endpoint to update a spaceship
@app.route('/api/spaceship/<int:id>', methods=['PUT'])
def update_spaceship(id):
    data = request.get_json()
    spaceship = Spaceship.query.get(id)
    if spaceship:
        spaceship.maxweight = data.get('maxweight', spaceship.maxweight)
        spaceship.captainid = data.get('captainid', spaceship.captainid)
        db.session.commit()
        result = SpaceshipSchema().dump(spaceship)
        return jsonify(result)
    return jsonify({'message': 'Spaceship not found'}), 404

# Spaceship endpoint to delete a spaceship
@app.route('/api/spaceship/<int:id>', methods=['DELETE'])
def delete_spaceship(id):
    spaceship = Spaceship.query.get(id)
    if spaceship:
        db.session.delete(spaceship)
        db.session.commit()
        return jsonify(SpaceshipSchema().dump(spaceship, many=True))
    else:
        return jsonify({'error': 'Spaceship not found.'}), 404

# Get all captains
@app.route('/api/captains', methods=['GET'])
def get_all_captains():
    captains = Captain.query.all()
    return jsonify(CaptainSchema().dump(captains, many=True))

# Get single captain (detail view)
@app.route('/api/captain/<int:id>', methods=['GET'])
def get_captain(id):
    captain = Captain.query.get(id)
    if captain:
        return jsonify(CaptainSchema().dump(captain))
    else:
        return jsonify({'error': 'Captain not found.'}), 404

# Add new captain
@app.route('/api/captain', methods=['POST'])
def add_captain():
    data = request.get_json()
    new_captain = Captain(firstname=data['firstname'], lastname=data['lastname'], rank=data['rank'], homeplanet=data['homeplanet'])
    db.session.add(new_captain)
    db.session.commit()
    return jsonify(CaptainSchema().dump(new_captain))

# Update captain
@app.route('/api/captain/<int:id>', methods=['PUT'])
def update_captain(id):
    data = request.get_json()
    captain = Captain.query.get(id)
    if captain:
        captain.firstname = data.get('firstname', captain.firstname)
        captain.lastname = data.get('lastname', captain.lastname)
        captain.rank = data.get('rank', captain.rank)
        captain.homeplanet = data.get('homeplanet', captain.homeplanet)
        db.session.commit()
        return jsonify(CaptainSchema().dump(captain))
    else:
        return jsonify({'error': 'Captain not found.'}), 404

# Delete captain
@app.route('/api/captain/<int:id>', methods=['DELETE'])
def delete_captain(id):
    captain = Captain.query.get(id)
    if captain:
        db.session.delete(captain)
        db.session.commit()
        return jsonify(CaptainSchema().dump(captain))
    else:
        return jsonify({'error': 'Captain not found.'}), 404

if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    # run on port 5001 to avoid conflicts with other services
    app.run(debug=True, port=5001)
