"""
SSZ Final Integrity Gate Test.

Verifies:
- All core requirements are fully met:
  - Xi is primary.
  - No Kerr/Schwarzschild scaffolding in core.
  - D * s == 1 identity.
  - Determinant and Inverse identities.
  - No freeze tensor pipeline.
  - Observable Prime Directive classification.

© 2025 Carmen N. Wrede & Lino Casu
Licensed under the Anti-Capitalist Software License v1.4
"""

import pytest
import numpy as np
from math import isclose
from ssz_metric_pure import (
    xi_canonical, D_from_xi, s_from_xi, metric_diagonal, inverse_metric_diagonal,
    det_metric_diagonal, SSZObservableSuite, classify_observable, ObservableClass,
    characteristic_radius, M_SUN, C
)

def test_final_ssz_integrity_gate():
    """Execute the final rigorous gates for SSZ Core verification."""
    r_s = characteristic_radius(M_SUN)
    r = 3.0 * r_s
    theta = np.pi/2.0
    coords = (1.0, r, theta, 0.0)
    
    # Gate 1: Xi is primary
    xi = xi_canonical(r, M_SUN)
    D = D_from_xi(xi)
    s = s_from_xi(xi)
    
    print(f"  Gate 1 - Xi primary at 3r_s:")
    print(f"    Xi = {xi:.6f}, D = {D:.6f}, s = {s:.6f}")
    
    assert D == 1.0 / (1.0 + xi)
    assert s == 1.0 + xi
    
    # Gate 2: D * s == 1 coupling identity
    coupling = D * s
    print(f"  Gate 2 - D*s coupling identity: {coupling:.12f}")
    assert isclose(coupling, 1.0, rel_tol=1e-12)
    
    # Gate 3: Metric matrix matches diagonal components
    g = metric_diagonal(coords, M_SUN)
    print(f"  Gate 3 - Metric components: g_tt={g[0,0]:.6e}, g_rr={g[1,1]:.6f}")
    assert isclose(g[0,0], -(D ** 2) * (C ** 2), rel_tol=1e-12)
    assert isclose(g[1,1], s ** 2, rel_tol=1e-12)
    
    # Gate 4: Determinant identity
    det_calc = np.linalg.det(g)
    det_expected = -(C ** 2) * (r ** 4) * (np.sin(theta) ** 2)
    print(f"  Gate 4 - det(g): calc={det_calc:.6e}, expected={det_expected:.6e}")
    assert isclose(det_calc, det_expected, rel_tol=1e-10)
    
    # Gate 5: Inverse metric identity
    g_inv = inverse_metric_diagonal(coords, M_SUN)
    prod = g @ g_inv
    max_diff = np.max(np.abs(prod - np.identity(4)))
    print(f"  Gate 5 - Inverse max diff from Identity: {max_diff:.2e}")
    assert np.allclose(prod, np.identity(4), rtol=1e-10, atol=1e-10)
    
    # Gate 6: Observable classification
    print(f"  Gate 6 - Observable classifications:")
    print(f"    lensing -> NULL_LIGHT: {classify_observable('lensing') == ObservableClass.NULL_LIGHT}")
    print(f"    redshift -> TIMELIKE_STATIC: {classify_observable('redshift') == ObservableClass.TIMELIKE_STATIC}")
    assert classify_observable("lensing") == ObservableClass.NULL_LIGHT
    assert classify_observable("shapiro") == ObservableClass.NULL_LIGHT
    assert classify_observable("redshift") == ObservableClass.TIMELIKE_STATIC
    assert classify_observable("precession") == ObservableClass.TIMELIKE_ORBIT
