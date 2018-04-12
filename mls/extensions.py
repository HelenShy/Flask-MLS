from flask_debugtoolbar import DebugToolbarExtension
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_marshmallow import Marshmallow
from flask_mail import Mail

debug_toolbar = DebugToolbarExtension()
db = SQLAlchemy()
jwt = JWTManager()
ma = Marshmallow()
mail = Mail()

