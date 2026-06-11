"""
Test of Operational Segmentation Concepts.

Verifies:
- Xi(r) is non-negative and monotonically decreasing.
- D * s == 1 identically.
- Segment distance ρ(r1, r2) is finite, positive, monotonic and ρ > coordinate radial interval for Xi > 0.
- Local speed-of-light invariance (local c is invariant in orthonormal frames).
- C² continuity of Xi across blend zone boundaries (value, 1st and 2nd derivatives).

© 2025 Carmen N. Wrede & Lino Casu
Licensed under the Anti-Capitalist Software License v1.4
"""

import pytest
import numpy as np
from math import isclose
from ssz_metric_pure import (
    segment_density, segment_scale, segment_distance, local_orthonormal_speed_check,
    characteristic_radius, D_from_xi, s_from_xi, PHI, M_SUN, C
)

def test_segment_properties():
    """Verify segment density non-negativity and asymptotic properties."""
    r_s = characteristic_radius(M_SUN)
    r_vals = np.logspace(0, 5, 500) * r_s
    
    xi_vals = segment_density(r_vals, M_SUN)
    s_vals = segment_scale(r_vals, M_SUN)
    
    # 1. Non-negativity
    assert np.all(xi_vals >= 0.0)
    assert np.all(s_vals >= 1.0)
    
    # 2. Asymptotics: Xi -> 0 for large r
    assert isclose(xi_vals[-1], 0.0, abs_tol=1e-5)
    
    # 3. Monotonic decrease (Xi must strictly decrease or stay within floating point precision)
    diffs = np.diff(xi_vals)
    assert np.all(diffs <= 1e-12), f"Xi is not monotonic! Max diff: {np.max(diffs)}"


def test_algebraic_complementary_identity():
    """Verify that D * s == 1 is identically satisfied across all scales."""
    r_s = characteristic_radius(M_SUN)
    r_vals = np.logspace(0, 6, 500) * r_s
    
    for r in r_vals:
        xi = segment_density(r, M_SUN)
        D = D_from_xi(xi)
        s = s_from_xi(xi)
        
        assert isclose(D * s, 1.0, rel_tol=1e-12)


def test_segment_distance():
    """Verify that operational segment distance is finite, positive, and larger than radial coordinates."""
    r_s = characteristic_radius(M_SUN)
    r1 = 1.1 * r_s
    r2 = 1.7 * r_s
    
    coord_dist = r2 - r1
    seg_dist = segment_distance(r1, r2, M_SUN)
    
    # Segment distance must be strictly greater than coordinate distance since Xi > 0
    assert seg_dist > coord_dist
    assert seg_dist > 0


def test_local_c_invariance():
    """Verify local speed of light is identically c in orthonormal frames."""
    r_s = characteristic_radius(M_SUN)
    r_vals = np.linspace(1.1, 10.0, 100) * r_s
    
    for r in r_vals:
        local_speed = local_orthonormal_speed_check(r, M_SUN)
        assert isclose(local_speed, C, rel_tol=1e-12)


def test_c2_blend_continuity():
    """Verify C² continuity of Segment Density at boundary nodes r/r_s = 1.8 and 2.2."""
    r_s = characteristic_radius(M_SUN)
    h = 1e-6
    
    # 1. Node 1.8 r_s (Strong vs Blended)
    node_18 = 1.8 * r_s
    
    # Values
    xi_strong_18 = segment_density(node_18 - h, M_SUN)
    xi_blend_18 = segment_density(node_18 + h, M_SUN)
    assert isclose(xi_strong_18, xi_blend_18, rel_tol=1e-5)
    
    # First derivatives
    d1_strong = (segment_density(node_18, M_SUN) - segment_density(node_18 - h, M_SUN)) / h
    d1_blend = (segment_density(node_18 + h, M_SUN) - segment_density(node_18, M_SUN)) / h
    assert isclose(d1_strong, d1_blend, rel_tol=1e-3)
    # The derivative must be strictly negative!
    assert d1_strong < 0.0
    
    # Second derivatives
    d2_strong = (segment_density(node_18, M_SUN) - 2.0*segment_density(node_18 - h, M_SUN) + segment_density(node_18 - 2.0*h, M_SUN)) / (h**2)
    d2_blend = (segment_density(node_18 + 2.0*h, M_SUN) - 2.0*segment_density(node_18 + h, M_SUN) + segment_density(node_18, M_SUN)) / (h**2)
    assert isclose(d2_strong, d2_blend, rel_tol=1e-2, abs_tol=1e-3)
    
    # 2. Node 2.2 r_s (Blended vs Weak)
    node_22 = 2.2 * r_s
    
    # Values
    xi_blend_22 = segment_density(node_22 - h, M_SUN)
    xi_weak_22 = segment_density(node_22 + h, M_SUN)
    assert isclose(xi_blend_22, xi_weak_22, rel_tol=1e-5)
    
    # First derivatives
    d1_blend_22 = (segment_density(node_22, M_SUN) - segment_density(node_22 - h, M_SUN)) / h
    d1_weak_22 = (segment_density(node_22 + h, M_SUN) - segment_density(node_22, M_SUN)) / h
    assert isclose(d1_blend_22, d1_weak_22, rel_tol=1e-3)
    # The derivative must be strictly negative!
    assert d1_blend_22 < 0.0
    
    # Second derivatives
    d2_blend_22 = (segment_density(node_22, M_SUN) - 2.0*segment_density(node_22 - h, M_SUN) + segment_density(node_22 - 2.0*h, M_SUN)) / (h**2)
    d2_weak_22 = (segment_density(node_22 + 2.0*h, M_SUN) - 2.0*segment_density(node_22 + h, M_SUN) + segment_density(node_22, M_SUN)) / (h**2)
    assert isclose(d2_blend_22, d2_weak_22, rel_tol=1e-2, abs_tol=1e-3)
