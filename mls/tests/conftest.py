import pytest

from mls.app import create_app


@pytest.yield_fixture(scope='session')
def app():
    """
    Setup test app for the whole session.
    :return: Flask app
    """
    params = {
        'DEBUG':False,
        'TESTING':True,
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


# docker-compose exec website py.test mls/tests
