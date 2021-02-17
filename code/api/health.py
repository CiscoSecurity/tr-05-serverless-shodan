import requests
from http import HTTPStatus
from flask import Blueprint, current_app

from api.utils import jsonify_data
from api.errors import (
    ShodanUnexpectedError,
    ShodanInternalServerError,
    ShodanNotFoundError,
    ShodanSSLError
)

health_api = Blueprint('health', __name__)


@health_api.route('/health', methods=['POST'])
def health():
    try:
        response = requests.head(current_app.config['SHODAN_UI_URL'],
                                 headers=current_app.config['CTR_HEADERS'])
    except requests.exceptions.SSLError as error:
        raise ShodanSSLError(error)

    if response.ok:
        return jsonify_data({'status': 'ok'})

    else:
        expected_response_errors = {
            HTTPStatus.NOT_FOUND: ShodanNotFoundError,
            HTTPStatus.INTERNAL_SERVER_ERROR: ShodanInternalServerError
        }
        if response.status_code in expected_response_errors:
            raise expected_response_errors[response.status_code]
        else:
            raise ShodanUnexpectedError(response)
