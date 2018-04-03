from flask import Flask, Blueprint
from flask_restplus import Api, Resource

from mls.blueprints.auth.views import blueprint as api
from mls.extensions import debug_toolbar


def create_app(settings_override=None):
    """
    Create a Flask application using app factory pattern.

    :return: Flask app
    """
    app = Flask(__name__, instance_relative_config=True)
    # api = Api(app)

    app.config.from_object('config.settings')
    app.config.from_pyfile('settings.py', silent=True)

    if settings_override:
        app.config.update(settings_override)

    app.register_blueprint(api)
    extensions(app)

    # @api.route('/hi')
    # class HiWorld(Resource):
    #     def get(self):
    #         return {'hi': 'world'}

    return app


def extensions(app):
    """
    Register extensions on the app
    :param app: Flask app
    :return: None
    """
    debug_toolbar.init_app(app)
    return None
