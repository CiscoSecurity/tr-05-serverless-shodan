from api.errors import INVALID_ARGUMENT
from pytest import fixture

from app import app


@fixture(scope='session')
def client():
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
