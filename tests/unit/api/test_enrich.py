from http import HTTPStatus

from pytest import fixture

from tests.unit.api.utils import headers


def routes():
    yield '/deliberate/observables'
    yield '/observe/observables'
    yield '/refer/observables'


@fixture(scope='module', params=routes(), ids=lambda route: f'POST {route}')
def route(request):
    return request.param


@fixture(scope='module')
def invalid_json():
    return [{'type': 'domain'}]


def test_enrich_call_with_invalid_json_failure(
        route, client,  invalid_json, invalid_json_expected_payload, valid_jwt
):
    response = client.post(route, headers=headers(valid_jwt), json=invalid_json)

    assert response.status_code == HTTPStatus.OK
    assert response.json == invalid_json_expected_payload


@fixture(scope='module')
def valid_json():
    return [{'type': 'ip', 'value': '185.53.179.29'}]


def test_enrich_call_success(
        route, client,  valid_json, valid_jwt, success_expected_payload
):
    response = client.post(route, headers=headers(valid_jwt), json=valid_json)
    assert response.status_code == HTTPStatus.OK
    assert response.json == success_expected_payload
