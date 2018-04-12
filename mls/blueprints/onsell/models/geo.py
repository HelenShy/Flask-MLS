from mls.extensions import db, ma
from lib.util_sqlalchemy import LightResourceMixin


class Geo(db.Model, LightResourceMixin):
    __tablename__ = 'geo'

    id = db.Column(db.Integer, primary_key=True)
    lot_id = db.Column(db.Integer, db.ForeignKey('lots.id'))
    lat = db.Column(db.Integer)
    lng = db.Column(db.Integer)

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_by_lot_id(cls, lot_id):
        return cls.query.filter_by(lot_id=lot_id).first()

    @classmethod
    def all(cls):
        return cls.query.all()


class GeoSchema(ma.ModelSchema):
    class Meta:
        model = Geo
        fields = ('lat', 'lng')