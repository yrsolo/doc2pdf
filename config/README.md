# Config

This directory stores non-secret configuration files that are safe to keep in git.

Files:
- `repository.env` - checked-in repository metadata used by local automation
- `runtime.env.example` - non-secret runtime defaults and examples

Secrets must stay in local `.env` files or a secret manager.
