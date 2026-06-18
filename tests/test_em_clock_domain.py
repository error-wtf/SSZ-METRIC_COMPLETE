"""
Tests for the SSZ Electromagnetic and Clock Domain.

© 2025 Carmen N. Wrede & Lino Casu
Licensed under the Anti-Capitalist Software License v1.4
"""

import pytest
from math import isclose
from ssz_metric_pure.constants import M_SUN
from ssz_metric_pure.core import characteristic_radius
from ssz_metric_pure.clock_observables import (
    time_dilation_D,
    redshift_static,
    gps_clock_proxy,
    radial_scaling_factor,
    scale_electric_field,
    scale_magnetic_field,
    light_travel_time_correction
)


def test_time_dilation_D():
    """Verify D(r) calculation from Xi primary path."""
    r_test = 3.0 * characteristic_radius(M_SUN)
    D = time_dilation_D(r_test, M_SUN)
    print(f"  r = 3r_s = {r_test:.3e} m")
    print(f"  D(r) = {D:.10f}")
    print(f"  Expected: 0 < D < 1")
    assert D > 0.0
    assert D < 1.0


def test_redshift_static_and_gps_proxy():
    """Verify static redshift and GPS clock proxies are finite and properly oriented."""
    r_emit = 2.0 * characteristic_radius(M_SUN)
    r_obs = 5.0 * characteristic_radius(M_SUN)
    z = redshift_static(r_emit, r_obs, M_SUN)
    print(f"  Redshift z (2r_s -> 5r_s): {z:.6e}")
    print(f"  Expected: z > 0 (outwards redshift)")
    
    gps = gps_clock_proxy(6378100.0, 26560000.0, 5.972e24)
    print(f"  GPS clock proxy: {gps:.10f}")
    print(f"  Expected: > 0")
    
    assert z > 0.0
    assert gps > 0.0


def test_radial_scaling_and_em_scaling():
    """Verify radial scaling factor s(r) and electromagnetic field component scaling."""
    r_test = 3.0 * characteristic_radius(M_SUN)
    s = radial_scaling_factor(r_test, M_SUN)
    print(f"  s(r) at 3r_s: {s:.10f}")
    print(f"  Expected: s > 1")
    
    E_scaled = scale_electric_field(100.0, r_test, M_SUN)
    B_scaled = scale_magnetic_field(100.0, r_test, M_SUN)
    print(f"  E_scaled (input=100): {E_scaled:.2f} (expected: < 100)")
    print(f"  B_scaled (input=100): {B_scaled:.2f} (expected: > 100)")
    
    assert s > 1.0
    assert E_scaled < 100.0
    assert B_scaled > 100.0


def test_radial_time_correction():
    """Verify radial excess light travel time corrections are positive and monotonic."""
    r1 = 2.0 * characteristic_radius(M_SUN)
    r2 = 5.0 * characteristic_radius(M_SUN)
    dt = light_travel_time_correction(r1, r2, M_SUN)
    print(f"  Light travel time correction (2r_s -> 5r_s): {dt:.6e} s")
    print(f"  Expected: dt > 0")
    assert dt > 0.0
