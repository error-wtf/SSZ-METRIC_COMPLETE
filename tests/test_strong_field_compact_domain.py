"""
Tests for the SSZ Strong-Field and Compact Scale Domain.

© 2025 Carmen N. Wrede & Lino Casu
Licensed under the Anti-Capitalist Software License v1.4
"""

import pytest
import numpy as np
from math import isclose
from ssz_metric_pure.constants import M_SUN, PHI
from ssz_metric_pure.core import characteristic_radius
from ssz_metric_pure.strong_field import (
    Xi_at_schwarzschild_radius,
    D_at_schwarzschild_radius,
    strong_field_regime_report,
    compactness_report,
    finite_boundary_report,
    energy_condition_regime
)


def test_schwarzschild_radius_evaluations():
    """Verify primary and derivative potentials at exact horizon scaling node."""
    xi_rs = Xi_at_schwarzschild_radius(M_SUN)
    # Xi_strong(r_s) = 1 - e^-phi
    expected_xi = 1.0 - np.exp(-PHI)
    D_rs = D_at_schwarzschild_radius(M_SUN)
    expected_D = 1.0 / (1.0 + expected_xi)
    
    print(f"  Xi(r_s) = {xi_rs:.6f} (expected: {expected_xi:.6f})")
    print(f"  D(r_s) = {D_rs:.6f} (expected: {expected_D:.6f})")
    print(f"  D is FINITE at horizon: {D_rs:.6f} > 0")
    
    assert isclose(xi_rs, expected_xi, rel_tol=1e-12)
    assert isclose(D_rs, expected_D, rel_tol=1e-12)
    assert D_rs > 0.0


def test_regime_and_compactness_reports():
    """Verify strong field boundary and geometric compactness categorization reports."""
    r_s = characteristic_radius(M_SUN)
    
    rep = strong_field_regime_report(1.5 * r_s, M_SUN)
    rep_blend = strong_field_regime_report(2.0 * r_s, M_SUN)
    comp = compactness_report(10.0 * r_s, M_SUN)
    
    print(f"  Regime at 1.5r_s: {rep['regime']}")
    print(f"  Regime at 2.0r_s: {rep_blend['regime']}")
    print(f"  Compactness at 10r_s: {comp['compactness_ratio']:.1f} (expected: 0.1)")
    
    assert rep["regime"] == "STRONG_FIELD_CORE"
    assert rep_blend["regime"] == "BLEND_ZONE"
    assert isclose(comp["compactness_ratio"], 0.1, rel_tol=1e-12)


def test_finite_boundary_report():
    """Verify boundary evaluation at r_s."""
    b_rep = finite_boundary_report(M_SUN)
    print(f"  Xi_boundary = {b_rep['Xi_boundary']:.6f}")
    print(f"  D_boundary = {b_rep['D_boundary']:.6f} (FINITE!)")
    assert "Xi_boundary" in b_rep
    assert "D_boundary" in b_rep


def test_energy_condition_regime():
    """Verify proxy energy condition checks are finite and correct."""
    r_test = 3.0 * characteristic_radius(M_SUN)
    val = energy_condition_regime(r_test, M_SUN)
    print(f"  Energy condition at 3r_s: {val:.1f} (expected: 1.0)")
    assert val == 1.0
