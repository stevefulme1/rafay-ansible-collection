# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type


class ModuleDocFragment(object):
    DOCUMENTATION = r'''
options:
  api_key:
    description:
    - Rafay API key for authentication.
    - If not set, the value of the C(RAFAY_API_KEY) environment variable is used.
    - Required if I(api_bearer_token) is not provided.
    type: str
  api_secret:
    description:
    - Rafay API secret for authentication.
    - If not set, the value of the C(RAFAY_API_SECRET) environment variable is used.
    - Required if I(api_bearer_token) is not provided.
    type: str
  api_bearer_token:
    description:
    - Bearer token for OAuth2 or OIDC workload identity authentication.
    - When provided, I(api_key) and I(api_secret) are not required.
    - If not set, the value of the C(RAFAY_API_BEARER_TOKEN) environment variable is used.
    - Supports zero-trust, sovereign cloud, and secure AI factory deployments.
    type: str
  api_url:
    description:
    - URL of the Rafay API endpoint.
    - If not set, the value of the C(RAFAY_API_URL) environment variable is used.
    type: str
    default: https://console.rafay.dev/v3
  project:
    description:
    - Rafay project name to scope operations to.
    - If not set, the value of the C(RAFAY_PROJECT) environment variable is used.
    type: str
  validate_certs:
    description:
    - Whether to validate TLS certificates for the API endpoint.
    type: bool
    default: true
'''
