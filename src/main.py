#!/usr/bin/env python3
import argparse, json, sys
from src.worker import analyze_files

def main():
    ap = argparse.ArgumentParser(description="Multithreaded log analyzer")
    ap.add_argument("paths", nargs="+", help="One or more .txt log files")
    ap.add_argument("--lenient", action="store_true", help="Skip malformed lines instead of raising")
    ap.add_argument("--max-error-rate", type=float, default=0.05, help="Fail if global error rate exceeds this (default 0.05)")
    ap.add_argument("--max-p95", type=int, default=300, help="Fail if global p95 latency exceeds this (ms)")
    args = ap.parse_args()

    metrics = analyze_files(args.paths, maxsize=1000, strict=not args.lenient)
    print(json.dumps(metrics, indent=2))

    # Basic QA gate
    problems = []
    if metrics.get("total", 0) == 0:
        problems.append("No records parsed.")
    if metrics.get("error_rate", 0.0) > args.max_error_rate:
        problems.append(f"Global error rate too high: {metrics['error_rate']:.2%} > {args.max_error_rate:.2%}")
    p95 = metrics.get("p95_latency")
    if p95 is not None and p95 > args.max_p95:
        problems.append(f"Global p95 too high: {p95} ms > {args.max_p95} ms")

    if problems:
        print("\nCHECKS FAILED:")
        for p in problems:
            print(" -", p)
        sys.exit(1)
    else:
        print("\nCHECKS PASSED")
        sys.exit(0)

if __name__ == "__main__":
    main()
