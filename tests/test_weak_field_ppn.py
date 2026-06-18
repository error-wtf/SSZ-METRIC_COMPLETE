"""
Test Weak-Field Limit and PPN proximity of SSZ-Core.

Verifies:
- For U << 1, γ ≈ 1 + U + O(U²)
- Weak-field limit is close to GR PPN limits.

© 2025 Carmen N. Wrede & Lino Casu
Licensed under the Anti-Capitalist Software License v1.4
"""

import pytest
import numpy as np
from ssz_metric_pure import xi_canonical, gamma_from_xi, characteristic_radius, M_SUN, G, C

def test_weak_field_limit():
    """Verify that the Lorentz factor γ approaches 1 + U in the weak-field limit."""
    r_s = characteristic_radius(M_SUN)
    
    # Far-field region where U << 1
    r_far = 1e5 * r_s
    
    # Dimensionless potential U = r_s / (2r)
    U = r_s / (2.0 * r_far)
    
    xi = xi_canonical(r_far, M_SUN)
    gam = gamma_from_xi(xi)
    
    # Standard PPN expansion for the metric coefficient: g_rr = γ² ≈ 1 + 2U
    # Therefore, γ = 1 + Xi = 1 + U
    expected_gamma = 1.0 + U
    
    print(f"  r_far = {r_far:.3e} m (100,000 r_s)")
    print(f"  U = r_s/(2r) = {U:.6e}")
    print(f"  Xi(r_far) = {xi:.6e}")
    print(f"  Gamma = {gam:.10f}")
    print(f"  Expected (1+U) = {expected_gamma:.10f}")
    print(f"  Error = {abs(gam - expected_gamma):.2e}")
    
    # The relative difference must be extremely small
    assert abs(gam - expected_gamma) < 1e-15
