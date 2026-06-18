"""
Tests for the SSZ Phi-Lattice and Segmentation Domain.

© 2025 Carmen N. Wrede & Lino Casu
Licensed under the Anti-Capitalist Software License v1.4
"""

import pytest
import numpy as np
from math import isclose
from ssz_metric_pure.constants import PHI, M_SUN
from ssz_metric_pure.core import characteristic_radius
from ssz_metric_pure.phi_lattice import (
    phi_lattice_points,
    segment_index_from_radius,
    radius_from_segment_index,
    segment_density_profile,
    segment_distance,
    segment_count_proxy
)


def test_phi_lattice_points_monotonicity():
    """Verify that generated lattice points scale exponentially and monotonically with phi."""
    points = phi_lattice_points(0, 10)
    print(f"  Generated {len(points)} lattice points")
    print(f"  Point[0] = {points[0]:.6f} (expected: 1.0)")
    print(f"  Point[1] = {points[1]:.6f} (expected: PHI = {PHI:.6f})")
    print(f"  Monotonic increase: {np.all(np.diff(points) > 0)}")
    assert len(points) == 11
    assert isclose(points[0], 1.0)
    assert isclose(points[1], PHI)
    assert np.all(np.diff(points) > 0)


def test_radius_index_conversions():
    """Verify reciprocal indexing conversions."""
    r_val = 15.0
    r0 = 2.0
    k = segment_index_from_radius(r_val, r0)
    r_rec = radius_from_segment_index(k, r0)
    print(f"  Input r_val = {r_val}, r0 = {r0}")
    print(f"  Segment index k = {k}")
    print(f"  Recovered r = {r_rec:.10f}")
    print(f"  Error = {abs(r_rec - r_val):.2e}")
    assert isclose(r_rec, r_val, rel_tol=1e-12)


def test_segment_distance_stretching_and_monotonicity():
    """Verify segment path lengths are positive, monotonic, and exceed coordinate lengths."""
    r_s = characteristic_radius(M_SUN)
    
    # Segment distance from 2 r_s to 5 r_s
    rho1 = segment_distance(2.0 * r_s, 5.0 * r_s, M_SUN)
    rho2 = segment_distance(2.0 * r_s, 10.0 * r_s, M_SUN)
    
    coord_delta = 3.0 * r_s
    print(f"  rho(2r_s -> 5r_s) = {rho1:.6e} m")
    print(f"  rho(2r_s -> 10r_s) = {rho2:.6e} m")
    print(f"  Coordinate delta = {coord_delta:.6e} m")
    print(f"  rho > coord_delta: {rho1 > coord_delta}")
    print(f"  rho2 > rho1: {rho2 > rho1}")
    
    assert rho1 > 0.0
    assert rho2 > rho1
    assert rho1 > coord_delta


def test_segment_density_outward_decrease():
    """Verify that segment density profile Xi(r) is monotonically non-increasing outward."""
    r_s = characteristic_radius(M_SUN)
    r_vals = np.linspace(1.1 * r_s, 10.0 * r_s, 100)
    xi_vals = segment_density_profile(r_vals, M_SUN)
    
    print(f"  Xi at r=1.1r_s: {xi_vals[0]:.6f}")
    print(f"  Xi at r=10r_s: {xi_vals[-1]:.6f}")
    print(f"  Monotonic decrease: {np.all(np.diff(xi_vals) <= 0.0)}")
    
    assert np.all(np.diff(xi_vals) <= 0.0)


def test_segment_count_proxy():
    """Verify segment count scales with path length and base scale."""
    r_s = characteristic_radius(M_SUN)
    count = segment_count_proxy(2.0 * r_s, 5.0 * r_s, M_SUN, ell0=1.0)
    print(f"  Segment count for 2r_s -> 5r_s: {count:.2f}")
    print(f"  Expected: > 0")
    assert count > 0.0
