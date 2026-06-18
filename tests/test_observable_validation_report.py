"""
Tests for the SSZ Observable Validation Report Generator.

© 2025 Carmen N. Wrede & Lino Casu
Licensed under the Anti-Capitalist Software License v1.4
"""

import pytest
from ssz_metric_pure.observable_validation import run_full_validation_suite


def test_validation_suite_execution():
    """Verify that running the validation suite completes and passes all internal consistency checks."""
    suite = run_full_validation_suite()
    print(f"  Validation suite executed")
    print(f"  Total tests: {suite['summary']['total']}")
    print(f"  FAIL count: {suite['summary']['FAIL']}")
    assert "results" in suite
    assert "summary" in suite
    
    summary = suite["summary"]
    assert summary["total"] >= 9
    # Failures must be zero for perfect canonical core mathematical consistency
    assert summary["FAIL"] == 0
    
    for res in suite["results"]:
        assert "id" in res
        assert "name" in res
        assert "class" in res
        assert "method" in res
        assert "prediction" in res
        assert "reference_value" in res
        assert "difference" in res
        assert "status" in res
        assert "validation_type" in res
        
        # Verify status is not FAIL
        assert res["status"] in ("PASS", "PENDING")
        # Difference must be non-negative
        assert res["difference"] >= 0.0
