"""
Test of the Curvature Tensor and Connection Engine.

Verifies:
- The numeric connection differentiator is functional and robust.
- The tensor engine actually evaluates the metric function at perturbed coordinates
  rather than using static/frozen variables (No-Freeze-Tensor-Test).

© 2025 Carmen N. Wrede & Lino Casu
Licensed under the Anti-Capitalist Software License v1.4
"""

import pytest
import numpy as np
from ssz_metric_pure import (
    christoffel_symbols, einstein_tensor, metric_diagonal, M_SUN
)

def test_tensor_pipeline_no_freeze():
    """Verify that the curvature engine correctly differentiates with respect to coords."""
    # Define coordinate point (T, r, theta, phi)
    r_val = 10000.0  # 10 km
    theta_val = np.pi / 4.0  # 45 degrees
    coords = np.array([1.0, r_val, theta_val, 0.5])
    
    # 1. Correct dynamic metric function
    def dynamic_g_func(x):
        return metric_diagonal(x, M_SUN)
        
    Gamma_dynamic = christoffel_symbols(dynamic_g_func, coords)
    
    # 2. Artificially frozen metric function
    def frozen_g_func(x):
        return metric_diagonal(coords, M_SUN)
        
    Gamma_frozen = christoffel_symbols(frozen_g_func, coords)
    
    print(f"  r = {r_val:.1f} m, theta = {np.degrees(theta_val):.1f} deg")
    print(f"  Dynamic Gamma max: {np.max(np.abs(Gamma_dynamic)):.6e}")
    print(f"  Frozen Gamma max: {np.max(np.abs(Gamma_frozen)):.6e}")
    print(f"  Dynamic != Frozen: {not np.allclose(Gamma_dynamic, Gamma_frozen)}")
    
    # Under dynamic diagonal metric, Γ¹_00 should be non-zero
    assert not np.allclose(Gamma_dynamic, 0.0), "Dynamic connection symbols must be non-trivial"
    
    # For a frozen metric function, all Christoffel symbols must be zero
    assert np.allclose(Gamma_frozen, 0.0), "Frozen metric derivatives must produce zero connection"
    
    # The dynamic and frozen results must differ significantly!
    assert not np.allclose(Gamma_dynamic, Gamma_frozen), "Differentiator freeze check failed"
