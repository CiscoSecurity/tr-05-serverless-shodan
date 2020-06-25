INVALID_ARGUMENT = 'invalid argument'
UNKNOWN = 'unknown'
NOT_FOUND = 'not found'
INTERNAL = 'internal error'


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
