from statistics import quantiles
from collections import defaultdict
from typing import Iterable, Dict, Any
from .log_record import LogRecord

def compute_metrics(recs: Iterable[LogRecord]) -> Dict[str, Any]:
    recs = list(recs)
    total = len(recs)
    if total == 0:
        return {"total": 0, "error_rate": 0.0, "p95_latency": None, "by_endpoint": {}}

    errors = sum(1 for r in recs if r.status >= 400)
    latencies = sorted(r.latency_ms for r in recs)
    # 95th percentile: 100 quantiles -> index 94 (0-based)
    p95 = quantiles(latencies, n=100)[94]

    by_ep = defaultdict(lambda: {"count": 0, "errors": 0})
    for r in recs:
        b = by_ep[r.endpoint]
        b["count"] += 1
        b["errors"] += int(r.status >= 400)

    return {
        "total": total,
        "error_rate": errors / total,
        "p95_latency": p95,
        "by_endpoint": dict(by_ep),
    }
