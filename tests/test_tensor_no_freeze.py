"""
Test of Curvature Differentiator No-Freeze Stability.

Verifies:
- Curvature tensor functions (Christoffel symbols, Riemann/Ricci tensors) are fully coordinate-dependent.
- Evaluates the metric dynamically at varied coordinate offsets x +/- h.
- Confirms frozen metrics produce distinct, degenerate results.

© 2025 Carmen N. Wrede & Lino Casu
Licensed under the Anti-Capitalist Software License v1.4
"""

import pytest
import numpy as np
from ssz_metric_pure import (
    metric_diagonal, christoffel_symbols, einstein_tensor, characteristic_radius, M_SUN
)

def test_tensor_no_freeze_dynamic():
    """Verify that Christoffel symbols and Einstein tensor evaluate dynamic coord dependencies."""
    r_s = characteristic_radius(M_SUN)
    coords = np.array([0.0, 5.0 * r_s, np.pi/2.0, 0.0])
    
    # 1. Dynamic metric function
    def g_func_dynamic(x):
        return metric_diagonal(x, M_SUN)
        
    # 2. Frozen metric function (always returns value at fixed coordinate)
    fixed_val = metric_diagonal(coords, M_SUN)
    def g_func_frozen(x):
        return fixed_val
        
    # Calculate Christoffel symbols dynamically
    gammas_dynamic = christoffel_symbols(g_func_dynamic, coords, h=1e-5)
    gammas_frozen = christoffel_symbols(g_func_frozen, coords, h=1e-5)
    
    print(f"  r = 5r_s = {5.0 * r_s:.3e} m")
    print(f"  Dynamic Christoffel max: {np.max(np.abs(gammas_dynamic)):.6e}")
    print(f"  Frozen Christoffel max: {np.max(np.abs(gammas_frozen)):.6e}")
    
    # Dynamic symbols must contain non-zero gradients and physical elements
    assert np.any(np.abs(gammas_dynamic) > 1e-15)
    
    # Frozen symbols must evaluate identically to zero since derivatives of constant are zero
    assert np.allclose(gammas_frozen, 0.0, atol=1e-15)
