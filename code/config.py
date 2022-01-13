import json


class Config:
    settings = json.load(open('container_settings.json', 'r'))
    VERSION = settings['VERSION']

    CTR_HEADERS = {
        'User-Agent': (
            'SecureX Threat Response Integrations '
            '<tr-integrations-support@cisco.com>'
        )
    }

    SHODAN_UI_URL = 'https://www.shodan.io'

    SHODAN_SEARCH_URL = 'https://www.shodan.io/search?query={value}'

    SHODAN_BROWSE_URL = 'https://www.shodan.io/host/{ip}'

    SHODAN_OBSERVABLE_TYPES = {
        'ip': 'IP',
        'domain': 'domain',
    }
