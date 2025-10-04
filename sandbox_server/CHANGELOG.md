## [Unreleased]\n\n### Changed\n- Updated /read endpoint to truncate large file outputs (over 50KB) and append truncation notice.\n- Added file size and truncation metadata to /read responses.\n
# HermesAI Sandbox Server – Changelog

## v3.1.0 - 2025-10-02

### Added
- GitHub OAuth login flow now supports `target` passthrough via the `state` parameter.
- Backend validates and redirects users back to their original target after successful login.

### Security
- Validation added to ensure only relative paths are accepted as redirect targets, preventing open redirect vulnerabilities.

---

## v3.0.0

### Breaking Changes
- Deprecated `/execute-async` and `/execute-async/status` endpoints.
- Unified execution into `/execute`, now PTY-backed for true streaming.
- Dropped job status polling. All events now flow through WebSocket + log buffer.

### New Features
- **`/ws/workspace`**: unified WebSocket stream for commands + outputs.
- **`/workspace/logs`**: paginated log access with `offset` + `limit`.
- **`/execute`**: returns job_id, returncode, and first 50KB of stdout (stderr merged due to PTY).

### Infrastructure
- Updated `openai-action.yml` to reflect the new API.
- Updated `OPENAI-METAPROMPT.md` with guidance for GPT agents.
- Removed `execute_async.py` route implementation.

### Testing
- Replaced async tests with `/execute` equivalents.
- Updated WebSocket tests to validate both command and output event structures.
- All tests green (13/13).

---
This release marks HermesAI Sandbox Server **v3.0.0** with a simplified, unified execution model that matches both GPT and human terminal use cases.