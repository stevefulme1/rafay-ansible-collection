# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import json

from ansible.module_utils.basic import env_fallback
from ansible.module_utils.urls import fetch_url


rafay_argument_spec = dict(
    api_key=dict(
        fallback=(env_fallback, ['RAFAY_API_KEY']),
        type='str',
        required=False,
        no_log=True,
    ),
    api_secret=dict(
        fallback=(env_fallback, ['RAFAY_API_SECRET']),
        type='str',
        required=False,
        no_log=True,
    ),
    api_bearer_token=dict(
        fallback=(env_fallback, ['RAFAY_API_BEARER_TOKEN']),
        type='str',
        required=False,
        no_log=True,
    ),
    api_url=dict(
        fallback=(env_fallback, ['RAFAY_API_URL']),
        type='str',
        default='https://console.rafay.dev/v3',
    ),
    project=dict(
        fallback=(env_fallback, ['RAFAY_PROJECT']),
        type='str',
    ),
    validate_certs=dict(type='bool', default=True),
)


class RafayModule:
    """Base class for Rafay API interactions."""

    def __init__(self, module):
        self.module = module
        self.api_url = module.params['api_url'].rstrip('/')
        self.bearer_token = module.params.get('api_bearer_token')
        self.project = module.params.get('project')

        if self.bearer_token:
            self.auth_header = 'Bearer {0}'.format(self.bearer_token)
        else:
            api_key = module.params.get('api_key')
            api_secret = module.params.get('api_secret')
            if not api_key:
                module.fail_json(
                    msg='api_key is required when api_bearer_token is not provided'
                )
            if not api_secret:
                module.fail_json(
                    msg='api_secret is required when api_bearer_token is not provided'
                )
            self.auth_header = 'Basic {0}'.format(
                __import__('base64').b64encode(
                    '{0}:{1}'.format(api_key, api_secret).encode()
                ).decode()
            )

    def request(self, method, path, data=None, query_params=None):
        """Make an authenticated request to the Rafay API."""
        url = '{0}{1}'.format(self.api_url, path)
        if query_params:
            url += '?' + '&'.join(
                '{0}={1}'.format(k, v) for k, v in query_params.items()
            )

        headers = {
            'Authorization': self.auth_header,
            'Content-Type': 'application/json',
            'Accept': 'application/json',
        }

        body = json.dumps(data) if data else None

        response, info = fetch_url(
            self.module,
            url,
            data=body,
            headers=headers,
            method=method,
            use_proxy=True,
        )

        status = info.get('status', -1)
        if status == -1:
            self.module.fail_json(
                msg='Failed to connect to Rafay API: {0}'.format(
                    info.get('msg', 'unknown error')
                )
            )

        response_body = response.read() if response else b''
        if response_body:
            try:
                return status, json.loads(response_body)
            except json.JSONDecodeError:
                return status, {'raw': response_body.decode('utf-8', errors='replace')}
        return status, {}

    def get(self, path, query_params=None):
        """GET request."""
        return self.request('GET', path, query_params=query_params)

    def post(self, path, data):
        """POST request."""
        return self.request('POST', path, data=data)

    def put(self, path, data):
        """PUT request."""
        return self.request('PUT', path, data=data)

    def delete(self, path):
        """DELETE request."""
        return self.request('DELETE', path)
