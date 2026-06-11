"""
Smoke tests for CLI execution of fetch_nicer.py and fetch_alma.py scripts.

© 2026 Carmen N. Wrede & Lino Casu
Licensed under the Anti-Capitalist Software License v1.4
"""

import subprocess
import pytest


def test_cli_help_options():
    """Verify that both fetch CLI scripts support standard --help argument and exit cleanly."""
    for script in ["scripts/fetch_nicer.py", "scripts/fetch_alma.py"]:
        res = subprocess.run(["python3", script, "--help"], capture_output=True, text=True)
        assert res.returncode == 0
        assert "usage:" in res.stdout or "options" in res.stdout
