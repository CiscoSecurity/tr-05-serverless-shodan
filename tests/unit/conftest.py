from datetime import datetime

from api.errors import INVALID_ARGUMENT

from authlib.jose import jwt
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


@fixture(scope='session')
def valid_jwt(client):
    header = {'alg': 'HS256'}

    payload = {'username': 'gdavoian', 'superuser': False}

    secret_key = client.application.secret_key

    return jwt.encode(header, payload, secret_key).decode('ascii')


@fixture(scope='session')
def invalid_jwt(valid_jwt):
    header, payload, signature = valid_jwt.split('.')

    def jwt_decode(s: str) -> dict:
        from authlib.common.encoding import urlsafe_b64decode, json_loads
        return json_loads(urlsafe_b64decode(s.encode('ascii')))

    def jwt_encode(d: dict) -> str:
        from authlib.common.encoding import json_dumps, urlsafe_b64encode
        return urlsafe_b64encode(json_dumps(d).encode('ascii')).decode('ascii')

    payload = jwt_decode(payload)

    # Corrupt the valid JWT by tampering with its payload.
    payload['superuser'] = True

    payload = jwt_encode(payload)

    return '.'.join([header, payload, signature])


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


@fixture(scope='module')
def success_expected_payload(route, client):
    if route.endswith('/refer/observables'):
        return {
            "data": [
                {
                    "categories": [
                        "Search",
                        "Shodan"
                    ],
                    "description": "Lookup this IP on Shodan",
                    "id": "ref-shodan-search-ip-185.53.179.29",
                    "title": "Search for this IP",
                    "url": "https://www.shodan.io/search?query=185.53.179.29"
                },
                {
                    "categories": [
                        "Browse",
                        "Shodan"
                    ],
                    "description": "Browse this IP on Shodan",
                    "id": "ref-shodan-detail-ip-185.53.179.29",
                    "title": "Browse IP",
                    "url": "https://www.shodan.io/host/185.53.179.29"
                }
            ]
        }

    else:
        return {'data': {}}
