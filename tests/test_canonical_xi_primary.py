"""
Test Canonical Xi Primary Principles and Regime Routing.

Verifies:
- At r = r_s, Xi_strong(r_s) == 1 - exp(-phi) within 1e-12 tolerance.
- For large r, Xi_weak(r) == r_s / (2r).
- Regime routing matches documentation specifications.
- Metric is built from Xi first (Xi-primary concept).

© 2025 Carmen N. Wrede & Lino Casu
Licensed under the Anti-Capitalist Software License v1.4
"""

import pytest
import numpy as np
from math import isclose
from ssz_metric_pure import (
    xi_strong, xi_weak, xi_canonical, D_from_xi, s_from_xi, regime_of_r,
    characteristic_radius, PHI, M_SUN, G, C
)

def test_canonical_xi_values():
    """Verify primary Segment Density boundary values and weak-field asymptotic scaling."""
    r_s = characteristic_radius(M_SUN)
    
    # 1. Strong-field value at Schwarzschild radius: Xi(r_s) == 1 - e^-phi
    xi_rs_analytical = 1.0 - np.exp(-PHI)
    xi_rs_numerical = xi_strong(r_s, M_SUN)
    assert isclose(xi_rs_numerical, xi_rs_analytical, rel_tol=1e-12)
    
    # 2. Weak-field values at r = 10, 100, 1000 r_s
    for scale in [10.0, 100.0, 1000.0]:
        r = scale * r_s
        xi_w = xi_weak(r, M_SUN)
        xi_c = xi_canonical(r, M_SUN)
        
        # Verify match with standard analytical decay
        expected = r_s / (2.0 * r)
        assert isclose(xi_w, expected, rel_tol=1e-12)
        assert isclose(xi_c, expected, rel_tol=1e-12)


def test_regime_routing():
    """Verify that regime routing matches canonical specifications."""
    r_s = characteristic_radius(M_SUN)
    
    assert regime_of_r(1.0 * r_s, M_SUN) == "very_close"
    assert regime_of_r(2.0 * r_s, M_SUN) == "blended"
    assert regime_of_r(2.5 * r_s, M_SUN) == "photon_sphere"
    assert regime_of_r(5.0 * r_s, M_SUN) == "strong"
    assert regime_of_r(100.0 * r_s, M_SUN) == "weak"


def test_xi_is_primary():
    """Verify that the scaling factors are built directly from Xi as the primary field."""
    r_s = characteristic_radius(M_SUN)
    r = 3.0 * r_s
    
    xi = xi_canonical(r, M_SUN)
    D = D_from_xi(xi)
    s = s_from_xi(xi)
    
    # Assert that D and s are derived mathematically and causally from Xi
    assert isclose(D, 1.0 / (1.0 + xi), rel_tol=1e-15)
    assert isclose(s, 1.0 + xi, rel_tol=1e-15)
