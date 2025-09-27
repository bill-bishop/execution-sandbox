# DropCode Sandbox Server – OpenAI Metaprompt

## Overview
The DropCode Sandbox Server provides a controlled environment where OpenAI agents (and human users) can execute shell commands, exchange files, and view logs in a shared workspace. Execution is designed to behave like a real terminal session while exposing APIs that fit OpenAI’s tool interface.

## Execution Model

### `/api/execute`
- The **only execution endpoint** exposed to OpenAI agents.
- Spawns the command in a **PTY** (pseudo-terminal) so output is flushed line-by-line and behaves like a real shell.
- Behavior:
  - Emits a **command event** immediately to the workspace log + WebSocket.
  - Streams all command output as **output events** to the workspace log + WebSocket.
  - Returns quickly (within a few seconds) with:
    - Job metadata.
    - Partial output collected so far.
    - `returncode = null` if the process is still running.
- Example response:
  ```json
  {
    "job_id": "...",
    "command": "pytest -q",
    "returncode": null,
    "stdout": "collected 2 items...\n--- Process still running, more output will stream via WebSocket ---"
  }
  ```
- Full output continues streaming via WebSocket or can be pulled from `/api/workspace/logs`.

### Deprecated Endpoints
- `/execute-async`, `/execute-async/status`, and `/execute/worker` are **not exposed to the OpenAI agent**.
- All agent-driven executions must use `/api/execute`.

## Workspace Stream

### WebSocket: `/ws/workspace`
- Shared live event stream for both GPT and human users.
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

### `/api/workspace/logs`
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

## File Management

### `/api/write`
- Create or overwrite a file with provided `filename` and `content`.

### `/api/read`
- Read the full content of a file.

### `/api/read-partial`
- Read a chunk of a file starting from an offset with optional limit.

## Agent Guidance
- Always use `/api/execute` for running commands.
- Expect partial output in the JSON response, but rely on `/ws/workspace` or `/api/workspace/logs` for complete logs.
- Never attempt to use `/execute-async`, `/status`, or `/worker`.
- To retrieve recent activity, use `/api/workspace/logs?offset=-20&limit=20`.

## Human + GPT Collaboration
- GPT and human users share the same PTY-backed terminal state.
- Human users see live output in the Terminal UI (via WebSocket).
- GPT can:
  - Use `/api/execute` for commands.
  - Follow `/ws/workspace` for real-time feedback.
  - Query `/api/workspace/logs` to review recent context.
  - Read/write files with `/api/read`, `/api/read-partial`, and `/api/write`.

This unified model ensures GPT and humans have the same visibility into the sandbox while avoiding long-blocking requests for the agent.