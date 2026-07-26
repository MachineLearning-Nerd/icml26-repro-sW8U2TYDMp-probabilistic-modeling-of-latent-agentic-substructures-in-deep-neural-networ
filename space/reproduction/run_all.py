"""Fixed command entrypoint. All evidence required for judgment is printed."""

from __future__ import annotations

import json
import os
import platform
import resource
import sys
import threading
import time

from .verifier import run_all


def main() -> int:
    started = time.perf_counter()
    started_usage = resource.getrusage(resource.RUSAGE_SELF)
    results = run_all()
    ended_usage = resource.getrusage(resource.RUSAGE_SELF)
    runtime = {
        "backend_contract": "local CPU for <=1 core and <5 minutes",
        "estimated_cores": 1,
        "selected_flavor": "local",
        "actual_python_threads": threading.active_count(),
        "logical_cpus_visible": os.cpu_count(),
        "runtime_seconds": time.perf_counter() - started,
        "user_cpu_seconds": ended_usage.ru_utime - started_usage.ru_utime,
        "system_cpu_seconds": ended_usage.ru_stime - started_usage.ru_stime,
        "max_rss_platform_units": ended_usage.ru_maxrss,
        "python": sys.version.split()[0],
        "platform": platform.platform(),
    }
    results["runtime"] = runtime
    print("=== REPRODUCTION_EVIDENCE_JSON_BEGIN ===")
    print(json.dumps(results, indent=2, sort_keys=True))
    print("=== REPRODUCTION_EVIDENCE_JSON_END ===")
    print(
        "SUMMARY "
        f"stage={results['campaign_stage']} "
        f"verified_or_falsified={results['full_credit_claims']}/6 "
        f"toy={results['toy_claims']}/6 "
        f"baseline_points={results['baseline_points']}/12 "
        f"runtime_s={runtime['runtime_seconds']:.6f} "
        f"estimated_cores=1 selected_flavor=local "
        f"python_threads={runtime['actual_python_threads']}"
    )
    return 0 if results["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
