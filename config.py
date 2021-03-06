import os

from __version__ import VERSION


class Config:
    VERSION = VERSION

    SECRET_KEY = os.environ.get('SECRET_KEY', '')

    CTR_HEADERS = {
        'User-Agent': (
            'SecureX Threat Response Integrations '
            '<tr-integrations-support@cisco.com>'
        )
    }

    SHODAN_UI_URL = 'http://www.shodan.io'

    SHODAN_SEARCH_URL = 'https://www.shodan.io/search?query={value}'

    SHODAN_BROWSE_URL = 'https://www.shodan.io/host/{ip}'

    SHODAN_OBSERVABLE_TYPES = {
        'ip': 'IP',
        'domain': 'domain',
    }
