# Multi-Threaded-Log-Analyzer
A small service that reads many log streams at the same time, parses each line into a structured record, and computes quality metrics (error rate, p95 latency, per-endpoint counts, etc.).

Goal: given N text streams (files, stdin pipes, sockets, etc.), produce metrics like:
* total requests
* error rate (HTTP status ≥ 400)
* p95 latency
* counts/errors per endpoint (e.g., GET /api/v1/items)