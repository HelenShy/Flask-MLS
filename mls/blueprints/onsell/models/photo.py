from mls.extensions import db, ma
from lib.util_sqlalchemy import LightResourceMixin

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])


class Photo(db.Model, LightResourceMixin):
    __tablename__ = 'photos'

    id = db.Column(db.Integer, primary_key=True)
    lot_id = db.Column(db.Integer, db.ForeignKey('lots.id'))
    photo_path = db.Column(db.String)

    def __init__(self, lot_id, photo_path):
        self.lot_id = lot_id
        self.photo_path = photo_path

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_by_lot_id(cls, lot_id):
        return cls.query.filter_by(lot_id=lot_id).all()

    @staticmethod
    def allowed_file(filename):
        return '.' in filename and \
               filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


class PhotoSchema(ma.ModelSchema):
    class Meta:
        model = Photo
