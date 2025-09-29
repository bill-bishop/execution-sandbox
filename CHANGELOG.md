# Changelog

## [Unreleased]
- TBD

## [0.2.0] - 2025-09-27
### Added
- Timeout enforcement for worker commands (default 60s, configurable via `COMMAND_TIMEOUT`).
- Tests for command timeout (`sleep` and hanging commands).
- Validation that timeout events are appended to `workspace_log`.

### Fixed
- Hanging PTY commands (e.g., `cat`, `sleep`) no longer cause indefinite blocking.
- Worker threads are properly killed after exceeding timeout.

## [0.1.0] - 2025-09-26
### Added
- Basic user authentication with JWT (`/auth/login`, `/me`).
- Workspace auto-creation on registration.
- `/auth/providers` endpoint for OAuth provider list.
- Initial Nginx config with regex-based user subdomain routing.
- Requirements pinned for stable fresh installs.
- Test coverage for authentication, workspace creation, and Nginx config.
