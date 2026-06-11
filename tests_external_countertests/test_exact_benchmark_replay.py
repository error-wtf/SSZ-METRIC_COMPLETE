"""
Tests for replaying exact benchmark records.

© 2026 Carmen N. Wrede & Lino Casu
Licensed under the Anti-Capitalist Software License v1.4
"""

import os
import subprocess


def test_exact_benchmark_replay():
    # Run the replay script
    script = "scripts/run_exact_benchmark_replay.py"
    res = subprocess.run([
        "python3", script,
        "--benchmark", "external_validation/countertests/benchmarks/exact_benchmark_observables.json"
    ], capture_output=True, text=True)
    assert res.returncode == 0
    assert "EXACT BENCHMARK REPLAY: PASS_EXACT" in res.stdout
