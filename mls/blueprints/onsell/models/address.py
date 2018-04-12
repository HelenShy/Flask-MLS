from mls.extensions import db, ma
from lib.util_sqlalchemy import LightResourceMixin


class Address(db.Model, LightResourceMixin):
    __tablename__ = 'address'

    id = db.Column(db.Integer, primary_key=True)
    lot_id = db.Column(db.Integer, db.ForeignKey('lots.id'))
    city = db.Column(db.String)
    street = db.Column(db.String)
    house_number = db.Column(db.Integer)

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_by_lot_id(cls, lot_id):
        return cls.query.filter_by(lot_id=lot_id).first()


class AddressSchema(ma.ModelSchema):
    class Meta:
        model = Address
