#!/usr/bin/python
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: rafay_user_info
short_description: Get Rafay user information
description:
  - Retrieve information about Rafay user resources.
  - Supports OIDC workload identity via bearer token authentication for zero-trust environments.
version_added: "1.0.0"
author:
  - Steve Fulmer (@stevefulme1)
options:
  username:
    description: The username of the resource.
    type: str
extends_documentation_fragment:
  - stevefulme1.rafay.rafay
"""

EXAMPLES = r"""
- name: Get all users
  stevefulme1.rafay.rafay_user_info:

- name: Get specific user
  stevefulme1.rafay.rafay_user_info:
    username: john.doe@example.com
"""

RETURN = r"""
resources:
  description: List of user resources.
  type: list
  returned: always
"""

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.stevefulme1.rafay.plugins.module_utils.rafay import (
    RafayModule,
    rafay_argument_spec,
)


def main():
    argument_spec = rafay_argument_spec.copy()
    argument_spec.update(
        username=dict(type='str'),
    )

    module = AnsibleModule(
        argument_spec=argument_spec,
        supports_check_mode=True,
    )

    rafay = RafayModule(module)
    path = '/auth/v3/user/'
    status, result = rafay.get(path)
    if status != 200:
        module.fail_json(msg='Failed to get resources', status=status)
    module.exit_json(changed=False, resources=result.get('items', [result]))


if __name__ == "__main__":
    main()
