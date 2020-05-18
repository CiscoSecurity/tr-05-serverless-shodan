from http import HTTPStatus

from pytest import fixture
from unittest import mock

from tests.unit.payloads_for_tests import (EXPECTED_RESPONSE_404_ERROR,
                                           EXPECTED_RESPONSE_500_ERROR)


def routes():
    yield '/health'


@fixture(scope='module', params=routes(), ids=lambda route: f'POST {route}')
def route(request):
    return request.param


@fixture(scope='function')
def shodan_request():
    with mock.patch('requests.head') as mock_request:
        yield mock_request


def shodan_response(*, ok, status_error=None):
    mock_response = mock.MagicMock()

    mock_response.ok = ok

    if ok:
        mock_response.status_code = 200
    else:
        if status_error == 404:
            mock_response.status_code = 404
        elif status_error == 500:
            mock_response.status_code = 500

    return mock_response


def test_health_call_success(route, client, shodan_request):
    shodan_request.return_value = shodan_response(ok=True)
    response = client.post(route)
    assert response.status_code == HTTPStatus.OK
    assert response.get_json() == {'data': {'status': 'ok'}}


def test_health_call_404(route, client, shodan_request):
    shodan_request.return_value = shodan_response(ok=False, status_error=404)
    response = client.post(route)
    assert response.status_code == HTTPStatus.OK
    assert response.get_json() == EXPECTED_RESPONSE_404_ERROR


def test_health_call_500(route, client, shodan_request):
    shodan_request.return_value = shodan_response(ok=False, status_error=500)
    response = client.post(route)
    assert response.status_code == HTTPStatus.OK
    assert response.get_json() == EXPECTED_RESPONSE_500_ERROR
