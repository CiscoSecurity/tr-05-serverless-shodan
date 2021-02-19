EXPECTED_RESPONSE_404_ERROR = {
    'errors': [
        {
            'code': 'not found',
            'message': 'The Shodan not found error occurred.',
            'type': 'fatal'
        }
    ]
}

EXPECTED_RESPONSE_500_ERROR = {
    'errors': [
        {
            'code': 'internal error',
            'message': 'The Shodan internal error occurred.',
            'type': 'fatal'
        }
    ]
}

EXPECTED_RESPONSE_SSL_ERROR = {
    'errors': [
        {
            'code': 'unknown',
            'message': 'Unable to verify SSL certificate: Self signed '
                       'certificate',
            'type': 'fatal'
        }
    ]
}

EXPECTED_WATCHDOG_ERROR = {
    'errors': [
        {
            'code': 'health check failed',
            'message': 'Invalid Health Check',
            'type': 'fatal'
        }
    ]
}
