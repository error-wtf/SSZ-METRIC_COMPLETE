"""
Test Diagonal SSZ-Core Metric.

Verifies:
- Determinant of diagonal form: det(g) == -c² * r⁴ * sin²θ (relative tolerance 1e-10)
- Inverse of diagonal form: g @ g_inv == I (tolerance 1e-10)

© 2025 Carmen N. Wrede & Lino Casu
Licensed under the Anti-Capitalist Software License v1.4
"""

import pytest
import numpy as np
from ssz_metric_pure import metric_diagonal, inverse_metric_diagonal, det_metric_diagonal, M_SUN, C

def test_metric_diagonal_properties():
    """Verify diagonal metric determinant and inverse identities."""
    # Choose some realistic test coordinates x = (T, r, theta, phi)
    r = 50000.0  # meters
    theta = np.pi / 3.0  # 60 degrees
    coords = (1.0, r, theta, 0.5)
    
    g = metric_diagonal(coords, M_SUN)
    g_inv = inverse_metric_diagonal(coords, M_SUN)
    
    # 1. Determinant identity: det(g) == -c² * r⁴ * sin²θ
    g_det_analytical = -(C ** 2) * (r ** 4) * (np.sin(theta) ** 2)
    g_det_numerical = np.linalg.det(g)
    
    relative_diff = abs(g_det_numerical - g_det_analytical) / abs(g_det_analytical)
    assert relative_diff < 1e-10
    
    # 2. Inverse identity: g @ g_inv == Identity Matrix
    prod = g @ g_inv
    identity = np.identity(4)
    
    assert np.allclose(prod, identity, rtol=1e-10, atol=1e-10)
