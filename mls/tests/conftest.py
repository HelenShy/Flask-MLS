import pytest

from mls.app import create_app
from mls.extensions import db as _db
from mls.blueprints.auth.models import User
from config import settings
import os


@pytest.yield_fixture(scope='session')
def app():
    """
    Setup test app for the whole session.
    :return: Flask app
    """
    basedir = os.path.abspath("./")
    db_uri = '{0}_test'.format(settings.SQLALCHEMY_DATABASE_URI)
    params = {
        'DEBUG': False,
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': db_uri,
        'SERVER_NAME': 'localhost:8000',
        'WTF_CSRF_ENABLED': False,
        'WTF_CSRF_METHODS': []
    }

    _app = create_app(settings_override=params)

    # Establish app context
    ctx = _app.app_context()
    ctx.push()

    yield _app

    ctx.pop()


@pytest.yield_fixture(scope='function')
def client(app):
    """
    Setup app client. It allows to trigger request to certain route
    and keep track of cookies (allows to run tests without browser)
    :param app: Pytest session fixture
    :return: Flask app client
    """
    yield app.test_client()


@pytest.fixture(scope='session')
def db(app):
    """
    Setup our database, this only gets executed once per session.

    :param app: Pytest fixture
    :return: SQLAlchemy database session
    """
    _db.drop_all()
    _db.create_all()

    # Create a single user because a lot of tests do not mutate this user.
    # It will result in faster tests.
    params = {
        #'role': 'admin',
        'email': 'admin@local.host',
        'password': 'devpassword',
        'username': 'admin'
    }

    admin = User(**params)

    _db.session.add(admin)
    _db.session.commit()

    return _db


@pytest.yield_fixture(scope='function')
def session(db):
    """
    Allow very fast tests by using rollbacks and nested sessions. This does
    require that your database supports SQL savepoints, and Postgres does.

    Read more about this at:
    http://stackoverflow.com/a/26624146

    :param db: Pytest fixture
    :return: None
    """
    db.session.begin_nested()

    yield db.session

    db.session.rollback()


# @pytest.fixture(scope='session')
# def token(db):
#     """
#     Serialize a JWS token.
#
#     :param db: Pytest fixture
#     :return: JWS token
#     """
#     user = User.find_by_username('admin')
#     return user.serialize_token()


# docker-compose exec website py.test mls/tests

