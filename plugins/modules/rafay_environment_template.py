#!/usr/bin/python
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: rafay_environment_template
short_description: Manage Rafay environment templates
description:
  - Create, update, and delete Rafay environment template resources.
  - Supports OIDC workload identity via bearer token authentication for zero-trust environments.
version_added: "1.0.0"
author:
  - Steve Fulmer (@stevefulme1)
options:
  name:
    description: The name of the resource.
    type: str
    required: true
  description:
    description: The description of the resource.
    type: str
  resources:
    description: The resources of the resource.
    type: list
  state:
    description: The state of the resource.
    type: str
    choices: ['present', 'absent']
    default: present
extends_documentation_fragment:
  - stevefulme1.rafay.rafay
"""

EXAMPLES = r"""
- name: Manage environment template
  stevefulme1.rafay.rafay_environment_template:
    name: my-environment_template
    state: present
"""

RETURN = r"""
resource:
  description: The environment_template resource object.
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
        description=dict(type='str'),
        resources=dict(type='list'),
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
    path = '/eaas/v3/project/{project}/environmenttemplate/{name}'.format(project=project, name=name, **module.params)

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
