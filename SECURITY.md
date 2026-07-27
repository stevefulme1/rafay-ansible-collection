# Security Policy

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 1.0.x   | :white_check_mark: |

## Reporting a Vulnerability

To report a security vulnerability, please email security@example.com or open a
[GitHub Security Advisory](https://github.com/stevefulme1/rafay-ansible-collection/security/advisories/new).

**Please do not report security vulnerabilities through public GitHub issues.**

We will acknowledge receipt within 48 hours and provide a detailed response within 5 business days.

## Security Best Practices

- Store Rafay API credentials in Ansible Vault or environment variables
- Use `no_log: true` for tasks containing sensitive data
- Enable TLS validation for all API connections (default behavior)
