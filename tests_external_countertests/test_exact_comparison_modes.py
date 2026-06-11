"""
Tests verifying exact comparison modes and tolerating procedures.

© 2026 Carmen N. Wrede & Lino Casu
Licensed under the Anti-Capitalist Software License v1.4
"""

import pytest
from ssz_metric_pure.external_exact_comparison import (
    compute_absolute_residual,
    compute_relative_residual,
    within_exact_tolerance,
    compare_exact,
    compare_uncertainty
)


def test_exact_comparison_modes():
    pred = {"value": 1.0000000000005}
    obs = {"value": 1.0, "comparison_mode": "EXACT_IDENTITY_MODE"}
    
    assert compute_absolute_residual(pred, obs) == pytest.approx(5e-13)
    assert compute_relative_residual(pred, obs) == pytest.approx(5e-13)
    
    # Tolerances
    assert within_exact_tolerance(pred, obs, abs_tol=1e-12, rel_tol=1e-10) is True
    assert within_exact_tolerance(pred, obs, abs_tol=1e-14, rel_tol=1e-15) is False
    
    # Exact classification
    res_ex = compare_exact(pred, obs, abs_tol=1e-12)
    assert res_ex["status"] == "PASS_EXACT"
    
    # Uncertainty mode
    obs_noisy = {"value": 1.0, "uncertainty": 0.1}
    res_unc = compare_uncertainty(pred, obs_noisy)
    assert res_unc["status"] == "PASS_UNCERTAINTY"
