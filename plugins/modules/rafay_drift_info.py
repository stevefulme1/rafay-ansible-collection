#!/usr/bin/python
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: rafay_drift_info
short_description: Get cluster configuration drift status
description:
  - Retrieve information about Rafay drift info resources.
  - Supports OIDC workload identity via bearer token authentication for zero-trust environments.
version_added: "1.0.0"
author:
  - Steve Fulmer (@stevefulme1)
options:
  cluster:
    description: The cluster of the resource.
    type: str
extends_documentation_fragment:
  - stevefulme1.rafay.rafay
"""

EXAMPLES = r"""
- name: Get drift info
  stevefulme1.rafay.rafay_drift_info:
    name: my-drift_info
"""

RETURN = r"""
resources:
  description: List of drift_info resources.
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
        cluster=dict(type='str'),
    )

    module = AnsibleModule(
        argument_spec=argument_spec,
        supports_check_mode=True,
    )

    rafay = RafayModule(module)
    project = module.params.get('project', 'default')
    path = '/infra/v3/project/{project}/drift/'.format(project=project)
    status, result = rafay.get(path)
    if status != 200:
        module.fail_json(msg='Failed to get resources', status=status)
    module.exit_json(changed=False, resources=result.get('items', [result]))


if __name__ == "__main__":
    main()
