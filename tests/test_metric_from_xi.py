"""
Test of Canonical Metric and Tensorial Properties Derived from Xi.

Verifies:
- Metric construction from primary Xi field.
- Determinant matches -c² * r⁴ * sin²θ exactly.
- Inverse matches Identity multiplication.

© 2025 Carmen N. Wrede & Lino Casu
Licensed under the Anti-Capitalist Software License v1.4
"""

import pytest
import numpy as np
from math import isclose
from ssz_metric_pure import (
    metric_diagonal, inverse_metric_diagonal, det_metric_diagonal,
    characteristic_radius, M_SUN, C
)

def test_metric_from_xi_construction():
    """Verify that the metric components and coordinates generate correct tensor values."""
    r_s = characteristic_radius(M_SUN)
    r = 5.0 * r_s
    theta = np.pi / 3.0  # 60 degrees
    coords = (1.0, r, theta, 0.2)
    
    g = metric_diagonal(coords, M_SUN)
    g_inv = inverse_metric_diagonal(coords, M_SUN)
    
    # 1. Determinant matches -c² * r⁴ * sin²θ
    det_analytical = det_metric_diagonal(coords, M_SUN)
    det_expected = -(C ** 2) * (r ** 4) * (np.sin(theta) ** 2)
    det_numerical = np.linalg.det(g)
    
    assert isclose(det_analytical, det_expected, rel_tol=1e-12)
    assert isclose(det_numerical, det_expected, rel_tol=1e-10)
    
    # 2. Inverse matches Identity
    prod = g @ g_inv
    identity = np.identity(4)
    assert np.allclose(prod, identity, rtol=1e-10, atol=1e-10)
