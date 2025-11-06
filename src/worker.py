import threading, queue
from typing import List, Dict, Any
from .parser import parse_file
from .log_record import LogRecord

def _producer(path: str, q: "queue.Queue[LogRecord | None]", strict: bool):
    for rec in parse_file(path, strict=strict):
        q.put(rec)                # backpressure if queue is full
    q.put(None)                   # sentinel for this producer

def _consumer(num_producers: int, q: "queue.Queue[LogRecord | None]") -> Dict[str, Any]:
    done = 0
    total = errors = 0
    latencies: list[int] = []
    by_ep: Dict[str, Dict[str, int]] = {}

    while done < num_producers:
        item = q.get()
        if item is None:
            done += 1
            q.task_done()
            continue
        total += 1
        if item.status >= 400:
            errors += 1
        latencies.append(item.latency_ms)
        ep = by_ep.setdefault(item.endpoint, {"count": 0, "errors": 0})
        ep["count"] += 1
        ep["errors"] += int(item.status >= 400)
        q.task_done()

    latencies.sort()
    p95 = latencies[int(0.95 * (len(latencies) - 1))] if latencies else None
    return {
        "total": total,
        "error_rate": (errors / total) if total else 0.0,
        "p95_latency": p95,
        "by_endpoint": by_ep,
    }

def analyze_files(paths: List[str], maxsize: int = 1000, strict: bool = True) -> Dict[str, Any]:
    q: "queue.Queue[LogRecord | None]" = queue.Queue(maxsize=maxsize)
    producers = [threading.Thread(target=_producer, args=(p, q, strict), daemon=True) for p in paths]

    for t in producers: t.start()

    result_box: list[Dict[str, Any] | None] = [None]
    def run_consumer():
        result_box[0] = _consumer(len(producers), q)

    c = threading.Thread(target=run_consumer, daemon=True)
    c.start()

    for t in producers: t.join()
    q.join()
    c.join()
    return result_box[0] or {}
