# DropCode Sandbox Server – OpenAI Metaprompt

## Overview
The DropCode Sandbox Server provides a controlled environment where OpenAI agents (and human users) can execute shell commands, exchange files, and view logs in a shared workspace. Execution is designed to behave like a real terminal session while exposing APIs that fit OpenAI’s tool interface.

## Execution Model

### `/execute`
- The single endpoint for all command execution (synchronous + streaming).
- Spawns the command in a **PTY** (pseudo-terminal) so output is flushed line-by-line and behaves like a real shell.
- Behavior:
  - Emits a **command event** immediately to the workspace log + WebSocket.
  - Streams all command output as **output events** to the workspace log + WebSocket.
  - Buffers the first 50 KB of output for inclusion in the synchronous JSON response.
- Returns JSON after process completion:
  ```json
  {
    "job_id": "...",
    "command": "echo hello",
    "returncode": 0,
    "stdout": "hello\n",
    "stderr": ""
  }
  ```
- Note: Because PTY merges streams, `stderr` will usually be empty. All output appears in `stdout` and the event stream.

### Deprecated Endpoints
- `/execute-async` and `/execute-async/status` are deprecated.
- All executions should now use `/execute`.

## Workspace Stream

### WebSocket: `/ws/workspace`
- Shared stream for both GPT and human users.
- Emits ordered events with `seq_id`.
- Event types:
  - **Command event**:
    ```json
    {
      "seq_id": 101,
      "type": "command",
      "job_id": "...",
      "command": "pytest -q",
      "source": "api"
    }
    ```
  - **Output event**:
    ```json
    {
      "seq_id": 102,
      "type": "output",
      "job_id": "...",
      "command": "pytest -q",
      "source": "api",
      "stream": "stdout",
      "line": "collected 5 items"
    }
    ```

## Workspace Logs

### `/workspace/logs`
- Provides access to the rolling buffer of all workspace events (commands + output).
- Parameters:
  - `offset`: integer, absolute index (0-based) or negative for relative to tail.
  - `limit`: integer, max number of events (default 100).
- Response:
  ```json
  [
    { "seq_id": 200, "type": "command", "command": "pytest -q" },
    { "seq_id": 201, "type": "output", "line": "collected 5 items" }
  ]
  ```

## Agent Guidance
- Always use `/execute` for running commands.
- Expect partial output in the JSON response, but rely on `/ws/workspace` or `/workspace/logs` to access the complete log.
- Do not use `/execute-async` or `/status`; these are deprecated.
- To retrieve recent activity, use `/workspace/logs?offset=-20&limit=20`.

## Human + GPT Collaboration
- GPT and human users share the same PTY-backed terminal state.
- Human users see live output in the Terminal UI (via WebSocket).
- GPT can:
  - Use `/execute` for commands.
  - Follow `/ws/workspace` for real-time feedback.
  - Query `/workspace/logs` to review recent context.

This unified model eliminates the need for separate sync/async modes and ensures GPT has the same visibility into the sandbox as a human user.