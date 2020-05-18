from functools import partial

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


@enrich_api.route('/refer/observables', methods=['POST'])
def refer_observables():
    observables = get_observables()
    ips = [
        observable['value']
        for observable in observables
        if observable['type'] == 'ip'
    ]

    data = [
        {
            'id': f'ref-shodan-search-ip-{ip}',
            'title': 'Search for this IP',
            'description': 'Lookup this IP on Shodan',
            'url': current_app.config['SHODAN_SEARCH_URL'].format(ip=ip),
            'categories': ['Search', 'Shodan'],
        }
        for ip in map(lambda ip: quote(ip, safe=''), ips)
    ]

    return jsonify_data(data)
