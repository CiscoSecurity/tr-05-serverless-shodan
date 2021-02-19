INVALID_ARGUMENT = 'invalid argument'
UNKNOWN = 'unknown'
NOT_FOUND = 'not found'
INTERNAL = 'internal error'
HEALTH_CHECK_ERROR = 'health check failed'


class CTRBaseError(Exception):
    def __init__(self, code, message, type_='fatal'):
        super().__init__()
        self.code = code or UNKNOWN
        self.message = message or 'Something went wrong.'
        self.type_ = type_

    @property
    def json(self):
        return {'type': self.type_,
                'code': self.code.lower(),
                'message': self.message}


class ShodanUnexpectedError(CTRBaseError):
    def __init__(self, response):
        super().__init__(
            response.reason,
            'An error occurred on the Shodan side.'
        )


class ShodanInternalServerError(CTRBaseError):
    def __init__(self):
        super().__init__(
            INTERNAL,
            'The Shodan internal error occurred.'
        )


class ShodanNotFoundError(CTRBaseError):
    def __init__(self):
        super().__init__(
            NOT_FOUND,
            'The Shodan not found error occurred.'
        )


class BadRequestError(CTRBaseError):
    def __init__(self, message):
        super().__init__(
            INVALID_ARGUMENT,
            f'Invalid JSON payload received. {message}'
        )


class ShodanSSLError(CTRBaseError):
    def __init__(self, error):
        error = error.args[0].reason.args[0]
        message = getattr(error, 'verify_message', error.args[0]).capitalize()
        super().__init__(
            UNKNOWN,
            f'Unable to verify SSL certificate: {message}'
        )


class ShodanWatchdogError(CTRBaseError):
    def __init__(self):
        super().__init__(
            HEALTH_CHECK_ERROR,
            'Invalid Health Check'
        )
