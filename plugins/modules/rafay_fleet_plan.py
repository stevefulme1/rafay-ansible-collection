#!/usr/bin/python
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: rafay_fleet_plan
short_description: Manage Rafay fleet operations
description:
  - Create, update, and delete Rafay fleet plan resources.
  - Supports OIDC workload identity via bearer token authentication for zero-trust environments.
version_added: "1.0.0"
author:
  - Steve Fulmer (@stevefulme1)
options:
  name:
    description: The name of the resource.
    type: str
    required: true
  operation_type:
    description: The operation type of the resource.
    type: str
    choices: ['blueprint_upgrade', 'k8s_upgrade', 'addon_update']
  target_clusters:
    description: The target clusters of the resource.
    type: list
  phased:
    description: The phased of the resource.
    type: bool
    default: true
  state:
    description: The state of the resource.
    type: str
    choices: ['present', 'absent']
    default: present
extends_documentation_fragment:
  - stevefulme1.rafay.rafay
"""

EXAMPLES = r"""
- name: Manage fleet plan
  stevefulme1.rafay.rafay_fleet_plan:
    name: my-fleet_plan
    state: present
"""

RETURN = r"""
resource:
  description: The fleet_plan resource object.
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
        name=dict(type='str', required=True),
        operation_type=dict(type='str', choices=['blueprint_upgrade', 'k8s_upgrade', 'addon_update']),
        target_clusters=dict(type='list'),
        phased=dict(type='bool', default=True),
        state=dict(type='str', choices=['present', 'absent'], default='present'),
    )

    module = AnsibleModule(
        argument_spec=argument_spec,
        supports_check_mode=True,
    )

    rafay = RafayModule(module)
    name = module.params['name']
    state = module.params['state']
    project = module.params.get('project', 'default')
    path = '/infra/v3/project/{project}/fleetplan/{name}'.format(project=project, name=name, **module.params)

    status, existing = rafay.get(path)
    exists = status == 200 and existing.get('metadata', existing.get('name'))

    if state == 'absent':
        if exists:
            if not module.check_mode:
                rafay.delete(path)
            module.exit_json(changed=True)
        module.exit_json(changed=False)

    body = {'metadata': {'name': name, 'project': project}}
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
