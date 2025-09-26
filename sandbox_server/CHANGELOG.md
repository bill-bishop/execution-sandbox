# DropCode Sandbox Server – Changelog

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
This release marks DropCode Sandbox Server **v3.0.0** with a simplified, unified execution model that matches both GPT and human terminal use cases.