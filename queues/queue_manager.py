import json
from pathlib import Path

MSG_QUEUE = Path("queues/msg_queue.json")
PROCESSING_QUEUE = Path("queues/processing_queue.json")
FINAL_QUEUE = Path("queues/final_memory_queue.json")

# ---------- COMMON ----------
def _read(file):
    if not file.exists():
        return []

    with file.open("r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []


def _write(file, data):
    with file.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)


# ---------- MSG QUEUE ----------
def push_msg(data: dict):
    queue = _read(MSG_QUEUE)
    queue.append(data)
    _write(MSG_QUEUE, queue)


def pop_msg():
    queue = _read(MSG_QUEUE)

    if not queue:
        return None

    job = queue.pop(0)
    _write(MSG_QUEUE, queue)

    return job


# ---------- PROCESSING QUEUE ----------
def push_processing(data: dict):
    queue = _read(PROCESSING_QUEUE)
    queue.append(data)
    _write(PROCESSING_QUEUE, queue)


def pop_processing():
    queue = _read(PROCESSING_QUEUE)

    if not queue:
        return None

    job = queue.pop(0)
    _write(PROCESSING_QUEUE, queue)

    return job


def push_final(data: dict):
    queue = _read(FINAL_QUEUE)
    queue.append(data)
    _write(FINAL_QUEUE, queue)


def pop_final():
    queue = _read(FINAL_QUEUE)

    if not queue:
        return None

    job = queue.pop(0)
    _write(FINAL_QUEUE, queue)

    return job