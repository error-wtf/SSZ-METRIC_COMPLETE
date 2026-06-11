"""
Test of the Curvature Tensor and Connection Engine.

Verifies:
- The numeric connection differentiator is functional and robust.
- The tensor engine actually evaluates the metric function at perturbed coordinates
  rather than using static/frozen variables (No-Freeze-Tensor-Test).

© 2025 Carmen Wrede & Lino Casu
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
    
    # Under dynamic diagonal metric, Γ¹_00 = -0.5 * g¹¹ * ∂_r g_00 should be non-zero
    assert not np.allclose(Gamma_dynamic, 0.0), "Dynamic connection symbols must be non-trivial"
    
    # 2. Artificially frozen metric function (freezes the coordinate variable x to static values)
    def frozen_g_func(x):
        # Always returns the metric evaluated at the fixed coords point, ignoring perturbations!
        return metric_diagonal(coords, M_SUN)
        
    Gamma_frozen = christoffel_symbols(frozen_g_func, coords)
    
    # For a completely frozen metric function, all coordinate derivatives are zero,
    # so all Christoffel symbols must be identically zero!
    assert np.allclose(Gamma_frozen, 0.0), "Frozen metric derivatives must produce zero connection"
    
    # The dynamic and frozen results must differ significantly!
    assert not np.allclose(Gamma_dynamic, Gamma_frozen), "Differentiator freeze check failed"
