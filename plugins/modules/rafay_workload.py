#!/usr/bin/python
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: rafay_workload
short_description: Manage Rafay workloads
description:
  - Create, update, and delete Rafay workload resources.
  - Supports OIDC workload identity via bearer token authentication for zero-trust environments.
version_added: "1.0.0"
author:
  - Steve Fulmer (@stevefulme1)
options:
  name:
    description: The name of the resource.
    type: str
    required: true
  workload_type:
    description: The workload type of the resource.
    type: str
    choices: ['helm', 'yaml']
  namespace:
    description: The namespace of the resource.
    type: str
  repository:
    description: The repository of the resource.
    type: str
  chart_name:
    description: The chart name of the resource.
    type: str
  chart_version:
    description: The chart version of the resource.
    type: str
  values:
    description: The values of the resource.
    type: dict
  state:
    description: The state of the resource.
    type: str
    choices: ['present', 'absent']
    default: present
extends_documentation_fragment:
  - stevefulme1.rafay.rafay
"""

EXAMPLES = r"""
- name: Manage workload
  stevefulme1.rafay.rafay_workload:
    name: my-workload
    state: present
"""

RETURN = r"""
resource:
  description: The workload resource object.
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
        workload_type=dict(type='str', choices=['helm', 'yaml']),
        namespace=dict(type='str'),
        repository=dict(type='str'),
        chart_name=dict(type='str'),
        chart_version=dict(type='str'),
        values=dict(type='dict'),
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
    path = '/infra/v3/project/{project}/workload/{name}'.format(project=project, name=name, **module.params)

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
