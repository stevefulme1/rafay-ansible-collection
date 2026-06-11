#!/usr/bin/python
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: rafay_user
short_description: Manage Rafay users
description:
  - Create, update, and delete Rafay user resources.
  - Supports OIDC workload identity via bearer token authentication for zero-trust environments.
version_added: "1.0.0"
author:
  - Steve Fulmer (@stevefulme1)
options:
  username:
    description: The username of the resource.
    type: str
    required: true
  first_name:
    description: The first name of the resource.
    type: str
  last_name:
    description: The last name of the resource.
    type: str
  email:
    description: The email of the resource.
    type: str
  groups:
    description: The groups of the resource.
    type: list
    elements: str
  state:
    description: The state of the resource.
    type: str
    choices: ['present', 'absent']
    default: present
extends_documentation_fragment:
  - stevefulme1.rafay.rafay
"""

EXAMPLES = r"""
- name: Manage user
  stevefulme1.rafay.rafay_user:
    username: my-user
    state: present
"""

RETURN = r"""
resource:
  description: The user resource object.
  type: dict
  returned: on success
"""

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.stevefulme1.rafay.plugins.module_utils.rafay import (
    RafayModule,
    rafay_argument_spec,
)


def main():
    argument_spec = rafay_argument_spec.copy()
    argument_spec.update(
        username=dict(type='str', required=True),
        first_name=dict(type='str'),
        last_name=dict(type='str'),
        email=dict(type='str'),
        groups=dict(type='list', elements='str'),
        state=dict(type='str', choices=['present', 'absent'], default='present'),
    )

    module = AnsibleModule(
        argument_spec=argument_spec,
        supports_check_mode=True,
    )

    rafay = RafayModule(module)
    username = module.params['username']
    state = module.params['state']
    project = module.params.get('project', 'default')
    path = '/auth/v3/user/{username}'.format(project=project, username=username, **module.params)

    status, existing = rafay.get(path)
    exists = status == 200 and existing.get('metadata', existing.get('username'))

    if state == 'absent':
        if exists:
            if not module.check_mode:
                rafay.delete(path)
            module.exit_json(changed=True)
        module.exit_json(changed=False)

    body = {'metadata': {'name': username, 'project': project}}
    if exists:
        if not module.check_mode:
            rafay.put(path, body)
        module.exit_json(changed=True, resource=body)
    else:
        if not module.check_mode:
            status, result = rafay.post(path, body)
        module.exit_json(changed=True, resource=body)


if __name__ == "__main__":
    main()
