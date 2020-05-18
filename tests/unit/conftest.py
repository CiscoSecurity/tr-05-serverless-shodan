from datetime import datetime

from api.errors import INVALID_ARGUMENT
from pytest import fixture

from app import app


@fixture(scope='session')
def secret_key():
    # Generate some string based on the current datetime.
    return datetime.utcnow().isoformat()


@fixture(scope='session')
def client(secret_key):
    app.secret_key = secret_key

    app.testing = True

    with app.test_client() as client:
        yield client


@fixture(scope='module')
def invalid_json_expected_payload(route, client):
    if route.endswith('/refer/observables'):
        return {'errors': [
            {'code': INVALID_ARGUMENT,
             'message': "Invalid JSON payload received. "
                        "{0: {'value': ['Missing data for required field.']}}",
             'type': 'fatal'}
        ]}

    else:
        return {'data': {}}
