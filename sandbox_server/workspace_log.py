from typing import List, Dict

MAX_LOG_SIZE = 10000
log_buffer: List[Dict] = []
seq_counter = 0


def append_event(event: dict) -> dict:
    global seq_counter
    seq_counter += 1
    event["seq_id"] = seq_counter
    log_buffer.append(event)
    if len(log_buffer) > MAX_LOG_SIZE:
        log_buffer.pop(0)
    return event


def get_logs(offset: int = 0, limit: int = 100) -> List[Dict]:
    if not log_buffer:
        return []

    if offset < 0:
        start = max(len(log_buffer) + offset, 0)
    else:
        start = min(offset, len(log_buffer))

    end = min(start + limit, len(log_buffer))
    return log_buffer[start:end]