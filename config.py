import os

from version import VERSION


class Config:
    VERSION = VERSION

    SECRET_KEY = os.environ.get('SECRET_KEY', '')

    CTR_HEADERS = {
        'User-Agent': (
            'Cisco Threat Response Integrations '
            '<tr-integrations-support@cisco.com>'
        )
    }

    SHODAN_UI_URL = 'https://www.shodan.io'

    SHODAN_SEARCH_URL = 'https://www.shodan.io/search?query={ip}'
