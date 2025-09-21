# Changelog

## [Unreleased]
- Initial introduction of this CHANGELOG.

## [1.1.0] - 2025-09-18
### Added
- **Async Execution** endpoints:
  - `POST /execute-async` → start a long-running job.
  - `GET /execute-async/status/{job_id}` → check job status.
  - `GET /execute-async/log/{job_id}` → fetch job logs.
- **Partial File Reading** endpoint:
  - `GET /read-partial` → read files in chunks using offset/limit.
- Tests for async execution and partial reads.
- Documentation updates:
  - `openai-action.yml` extended with new endpoints.
  - `OPENAI-METAPROMPT.md` updated with async + partial read usage guidelines.

### Changed
- `app.py` is now the canonical entrypoint.
- `sandbox_server.py` marked as **deprecated** and defers to `app.py`.

### Fixed
- Restored API key authentication middleware.
- Synced `config.py` default API key with test suite (`default-secret-key`).

## [1.0.0]
- Initial implementation with `/execute`, `/read`, and `/write` endpoints.
- API key authentication system (middleware initially commented out).
- MetaPrompt and OpenAPI schema created.