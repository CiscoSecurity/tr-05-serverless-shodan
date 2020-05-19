from functools import partial
from collections import defaultdict

from flask import Blueprint, current_app
from urllib.parse import quote

from api.schemas import ObservableSchema
from api.utils import get_json, jsonify_data

enrich_api = Blueprint('enrich', __name__)


get_observables = partial(get_json, schema=ObservableSchema(many=True))


@enrich_api.route('/deliberate/observables', methods=['POST'])
def deliberate_observables():
    # There are no verdicts to extract.
    return jsonify_data({})


@enrich_api.route('/observe/observables', methods=['POST'])
def observe_observables():
    # Not implemented.
    return jsonify_data({})


def get_browse_pivot(ips):
    return [
        {
            'id': f'ref-shodan-detail-ip-{ip}',
            'title': 'Browse IP',
            'description': 'Browse this IP on Shodan',
            'url': current_app.config['SHODAN_BROWSE_URL'].format(ip=ip),
            'categories': ['Browse', 'Shodan'],
        }
        for ip in map(lambda ip: quote(ip, safe=''), ips)
    ]


def get_search_pivots(observables):
    return [
        {
            'id': f'ref-shodan-search-{type}-{value}',
            'title':
                'Search for this'
                f' {current_app.config["SHODAN_OBSERVABLE_TYPES"][type]}',
            'description':
                'Lookup this '
                f'{current_app.config["SHODAN_OBSERVABLE_TYPES"][type]}'
                ' on Shodan',
            'url': current_app.config['SHODAN_SEARCH_URL'].format(value=value),
            'categories': ['Search', 'Shodan'],
        }
        for value, type in observables.items()
    ]


def group_observables(relay_input):
    # Leave only unique (value, type) pairs grouped by value.

    observables = defaultdict(set)

    for observable in relay_input:
        value = observable['value']
        type = observable['type'].lower()

        # Discard any unsupported type.
        if type in current_app.config['SHODAN_OBSERVABLE_TYPES']:
            observables[value] = type

    return observables


@enrich_api.route('/refer/observables', methods=['POST'])
def refer_observables():
    relay_input = get_observables()
    observables = group_observables(relay_input)

    ips = [
        value
        for value, type in observables.items()
        if type == 'ip'
    ]

    data = []
    data += get_search_pivots(observables)
    data += get_browse_pivot(ips)

    return jsonify_data(data)
