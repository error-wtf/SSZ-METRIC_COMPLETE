"""
Smoke tests for CLI countertest scripts.

© 2026 Carmen N. Wrede & Lino Casu
Licensed under the Anti-Capitalist Software License v1.4
"""

import os
import subprocess


def test_cli_help_options():
    """Verify help menus execute successfully with 0 exit codes."""
    for script in [
        "scripts/run_external_metric_countertests.py",
        "scripts/build_external_parameter_manifest.py",
        "scripts/list_eligible_external_datasets.py",
        "scripts/run_exact_benchmark_replay.py"
    ]:
        res = subprocess.run(["python3", script, "--help"], capture_output=True, text=True)
        assert res.returncode == 0, f"Script {script} failed to print help menu."
        assert "show this help message" in res.stdout
