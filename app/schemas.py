from marshmallow import fields
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from app import Cargo, Spaceship, Captain


class CargoSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Cargo
        load_instance = True

    id = fields.Integer(dump_only=True)
    weight = fields.Float(required=True)
    cargotype = fields.String(required=True)
    departure = fields.DateTime()
    arrival = fields.DateTime()
    shipid = fields.Integer(required=True)


class SpaceshipSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Spaceship
        load_instance = True

    id = fields.Integer(dump_only=True)
    maxweight = fields.Float(required=True)
    captainid = fields.Integer(required=True)


class CaptainSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Captain
        load_instance = True

    id = fields.Integer(dump_only=True)
    firstname = fields.String(required=True)
    lastname = fields.String(required=True)
    rank = fields.String(required=True)
    homeplanet = fields.String(required=True)
