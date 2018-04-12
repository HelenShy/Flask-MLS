from mls.extensions import db, ma
from werkzeug.security import generate_password_hash, check_password_hash
from lib.util_sqlalchemy import ResourceMixin
from mls.blueprints.onsell.models.lot import Lot


class User(ResourceMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    email = db.Column(db.String(80))
    password = db.Column(db.String(180))
    lots = db.relationship(Lot, backref='lots', passive_deletes=True)

    def __init__(self, username, email, password):
        self.username = username
        self.password = User.encrypt_password(password)
        self.email = email

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    # @classmethod
    # def find_by_identity(cls, email):
    #     return cls.query.filter_by(email=email).first()

    @classmethod
    def all(cls):
        return cls.query.all()

    @staticmethod
    def encrypt_password(password):
        return generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)


class RevokedTokenModel(db.Model, ResourceMixin):
    __tablename__ = 'revoked_tokens'
    id = db.Column(db.Integer, primary_key=True)
    jti = db.Column(db.String(120))

    @classmethod
    def is_jti_blacklisted(cls, jti):
        query = cls.query.filter_by(jti=jti).first()
        return bool(query)


class UserSchema(ma.ModelSchema):
    class Meta:
        model = User
        fields = ('username', 'email', 'id', 'lots')

    # _links = ma.Hyperlinks({
    #     'self': ma.URLFor('user', id='<id>'),
    #     'collection': ma.URLFor('users')
    # })
