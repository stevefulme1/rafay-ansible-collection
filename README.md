# Ansible Collection: stevefulme1.rafay

Ansible modules and roles for managing the [Rafay](https://rafay.co) Kubernetes Operations Platform, Environment Manager, GPU PaaS, and related services.

## Overview

This collection provides 36 modules and 5 roles covering:

- **Cluster Lifecycle** — Create, import, upgrade, and manage Kubernetes clusters (EKS, AKS, GKE, OpenShift, bare-metal)
- **Blueprints & Fleet** — Standardize cluster configurations and execute fleet-wide operations
- **Workloads & GitOps** — Deploy Helm charts and YAML workloads with GitOps pipelines
- **Multi-Tenancy & IAM** — Manage projects, users, groups, RBAC roles, and SSO
- **Security** — Network policies, OPA/Gatekeeper, audit logs, and secret store integrations
- **Backup & DR** — Backup policies, restore operations, and disaster recovery drills
- **Environment Manager** — Self-service developer environments with Terraform + Kubernetes templates
- **Cost Management** — Cost visibility, chargeback, and optimization
- **GPU & AI Infrastructure** — GPU compute profiles, instances, and inference endpoints

## Authentication

All modules support three authentication methods:

```yaml
# API key + secret (traditional)
- stevefulme1.rafay.rafay_cluster_info:
    api_key: "{{ rafay_api_key }}"
    api_secret: "{{ rafay_api_secret }}"

# Bearer token (OAuth2 / OIDC workload identity)
- stevefulme1.rafay.rafay_cluster_info:
    api_bearer_token: "{{ oidc_token }}"

# Environment variables
# export RAFAY_API_KEY=...
# export RAFAY_API_SECRET=...
# export RAFAY_API_BEARER_TOKEN=...  (for OIDC)
```

OIDC bearer token support enables zero-trust, sovereign cloud, and secure AI factory deployments without static credentials.

## Requirements

- ansible-core >= 2.16
- Python >= 3.10
- `kubernetes.core` collection

## Installation

```bash
ansible-galaxy collection install stevefulme1.rafay
```

## Modules

| Module | Description |
|--------|-------------|
| `rafay_cluster` | Manage Kubernetes clusters |
| `rafay_cluster_info` | Get cluster information |
| `rafay_cluster_upgrade` | Upgrade cluster Kubernetes version |
| `rafay_node_group` | Manage cluster node groups |
| `rafay_cloud_credential` | Manage cloud provider credentials |
| `rafay_blueprint` | Manage cluster blueprints |
| `rafay_blueprint_info` | Get blueprint information |
| `rafay_addon` | Manage Kubernetes add-ons |
| `rafay_fleet_plan` | Manage fleet operations |
| `rafay_drift_info` | Get configuration drift status |
| `rafay_workload` | Manage workloads (Helm/YAML) |
| `rafay_namespace` | Manage namespaces |
| `rafay_pipeline` | Manage GitOps pipelines |
| `rafay_repository` | Manage Git/Helm repositories |
| `rafay_catalog` | Manage workload catalog |
| `rafay_project` | Manage projects |
| `rafay_user` | Manage users |
| `rafay_group` | Manage groups |
| `rafay_role` | Manage custom RBAC roles |
| `rafay_sso` | Manage SSO configuration |
| `rafay_network_policy` | Manage network policies |
| `rafay_opa_policy` | Manage OPA/Gatekeeper policies |
| `rafay_audit_info` | Get audit log entries |
| `rafay_secret_store` | Manage secret store integrations |
| `rafay_backup_policy` | Manage backup policies |
| `rafay_backup_job` | Manage backup jobs |
| `rafay_restore` | Restore from backups |
| `rafay_backup_location` | Manage backup storage locations |
| `rafay_environment` | Manage developer environments |
| `rafay_environment_template` | Manage environment templates |
| `rafay_resource_template` | Manage resource templates |
| `rafay_config_context` | Manage config contexts |
| `rafay_cost_profile` | Manage cost allocation profiles |
| `rafay_cost_info` | Get cost data |
| `rafay_gpu_profile` | Manage GPU compute profiles |
| `rafay_gpu_instance` | Manage GPU instances |

## Roles

| Role | Description |
|------|-------------|
| `cluster_deploy` | Deploy a production-ready cluster with blueprint, backup, and monitoring |
| `fleet_upgrade` | Execute phased fleet-wide Kubernetes upgrade with validation |
| `onboard_team` | Onboard a team with project, namespaces, RBAC, and cost tracking |
| `dr_drill` | Run disaster recovery drill with backup, restore, and validation |
| `gpu_provision` | Provision GPU infrastructure for AI workloads |

## License

GPL-3.0-or-later

## Author

Steve Fulmer ([@stevefulme1](https://github.com/stevefulme1))
