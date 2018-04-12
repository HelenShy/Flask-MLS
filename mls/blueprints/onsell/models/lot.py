from mls.extensions import db, ma
from lib.util_sqlalchemy import ResourceMixin
from .geo import GeoSchema
from .address import AddressSchema
from .photo import PhotoSchema
#from mls.blueprints.auth.models import User
from flask_jwt_extended import get_jwt_identity, current_user


class Lot(ResourceMixin, db.Model):
    __tablename__ = 'lots'

    id = db.Column(db.Integer, primary_key=True)
    agent_id = db.Column(db.Integer, db.ForeignKey('users.id', onupdate='CASCADE', ondelete='CASCADE'),
                         index=True, nullable=False)
    agent = db.relationship('User')

    type = db.Column(db.String)
    description = db.Column(db.String(80))
    square = db.Column(db.Integer)
    qty_rooms = db.Column(db.Integer)
    parking = db.Column(db.Boolean)
    garageSpaces = db.Column(db.Integer)
    year_built = db.Column(db.Integer)
    price = db.Column(db.Integer)
    # owner_id = db.Column(db.Integer, db.ForeignKey('owner.id', ),
    #                      nullable=False)
    photos = db.relationship('Photo', cascade="all,delete", backref='lot', lazy='dynamic')
    address = db.relationship("Address", backref="lot")
    geo = db.relationship("Geo", backref="lot")
    # from mls.blueprints.auth.models import User
    status = db.Column(db.String)

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def all(cls):
        return cls.query.all()

    @classmethod
    def editable(cls, id):
        current_user = get_jwt_identity()
        lot_owner = Lot.find_by_id(id).agent
        return current_user == lot_owner.username


class AgentSchema(ma.ModelSchema):
    class Meta:
        fields = ('username', 'email', 'id')


class LotSchema(ma.ModelSchema):
    class Meta:
        # model = Lot
        fields = ('type', 'description', 'square', 'qty_rooms', 'parking', 'garageSpaces', 'year_built', 'price',
                  'agent_id', 'agent')

    geo = ma.Nested(GeoSchema, only=['lat', 'lng'])
    address = ma.Nested(AddressSchema)
    agent = ma.Nested(AgentSchema)
    photos = ma.Nested(PhotoSchema(), many=True, only='photo_path')
    # _links = ma.Hyperlinks({
    #     'self': ma.URLFor('onsell.onsell_get_lot', _id='<id>'),
    #     'collection': ma.URLFor('onsell.onsell_all_lots'),
    # })









