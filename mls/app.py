from flask import Flask, Blueprint, jsonify
from celery import Celery

from mls.blueprints.auth.resources import auth_blueprint as auth
from mls.blueprints.onsell.resources import onsell_blueprint as onsell
from mls.blueprints.contact.resources import contact_blueprint as contact
from mls.blueprints.auth.models import RevokedTokenModel, User
from mls.extensions import debug_toolbar, mail, db, jwt, ma

CELERY_TASK_LIST = [
    'mls.blueprints.contact.tasks',
]


def create_celery_app(app=None):
    """
    Create a new Celery object and tie together the Celery config to the app`s
    config. Wrap all tasks in the context of the application.
    :param app: Flask app
    :return: Celery app
    """
    app = app or create_app()

    celery = Celery(app.import_name, broker=app.config['CELERY_BROKER_URL'],
                    include=CELERY_TASK_LIST)
    celery.conf.update(app.config)
    task_base = celery.Task

    class ContextTask(task_base):
        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return task_base.__call__(self, *args, **kwargs)

    celery.Task = ContextTask
    return celery


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

    app.register_blueprint(auth)
    app.register_blueprint(onsell)
    app.register_blueprint(contact)
    extensions(app)
    jwt_callbacks()

    return app


def extensions(app):
    """
    Register extensions on the app
    :param app: Flask app
    :return: None
    """
    debug_toolbar.init_app(app)
    db.init_app(app)
    jwt.init_app(app)
    ma.init_app(app)
    mail.init_app(app)

    return None

@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    jti = decrypted_token['jti']
    return RevokedTokenModel.is_jti_blacklisted(jti)


def jwt_callbacks():
    """
    Set up custom behavior for JWT based authentication.

    :return: None
    """
    @jwt.user_loader_callback_loader
    def user_loader_callback(identity):
        return User.query.filter((User.username == identity)).first()

    @jwt.unauthorized_loader
    def jwt_unauthorized_callback(self):
        response = {
            'error': {
                'message': 'Your auth token or CSRF token are missing'
            }
        }

        return jsonify(response), 401

    @jwt.expired_token_loader
    def jwt_expired_token_callback():
        response = {
            'error': {
                'message': 'Your auth token has expired'
            }
        }

        return jsonify(response), 401

    return None
