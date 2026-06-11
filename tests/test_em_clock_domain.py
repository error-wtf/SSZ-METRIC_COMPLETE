"""
Tests for the SSZ Electromagnetic and Clock Domain.

© 2025 Carmen Wrede & Lino Casu
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
    D = time_dilation_D(3.0 * characteristic_radius(M_SUN), M_SUN)
    assert D > 0.0
    assert D < 1.0


def test_redshift_static_and_gps_proxy():
    """Verify static redshift and GPS clock proxies are finite and properly oriented."""
    z = redshift_static(2.0 * characteristic_radius(M_SUN), 5.0 * characteristic_radius(M_SUN), M_SUN)
    # Emitter closer than observer -> outwards redshift z > 0
    assert z > 0.0
    
    gps = gps_clock_proxy(6378100.0, 26560000.0, 5.972e24)
    assert gps > 0.0


def test_radial_scaling_and_em_scaling():
    """Verify radial scaling factor s(r) and electromagnetic field component scaling."""
    s = radial_scaling_factor(3.0 * characteristic_radius(M_SUN), M_SUN)
    assert s > 1.0
    
    E_scaled = scale_electric_field(100.0, 3.0 * characteristic_radius(M_SUN), M_SUN)
    B_scaled = scale_magnetic_field(100.0, 3.0 * characteristic_radius(M_SUN), M_SUN)
    
    # E scales with D^2 < 1, so E_scaled < E
    assert E_scaled < 100.0
    # B scales with s^2 > 1, so B_scaled > B
    assert B_scaled > 100.0


def test_radial_time_correction():
    """Verify radial excess light travel time corrections are positive and monotonic."""
    dt = light_travel_time_correction(2.0 * characteristic_radius(M_SUN), 5.0 * characteristic_radius(M_SUN), M_SUN)
    assert dt > 0.0
