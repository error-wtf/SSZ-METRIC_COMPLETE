"""
Tests for Forward SSZ Observable Predictions.

Verifies:
1. Clocks / Time-dilation / Redshift: TIMELIKE_STATIC routing.
2. Lensing and Shapiro: NULL_LIGHT routing with PPN completion (1+gamma).
3. Perihelion: TIMELIKE_ORBIT routing using exact PPN orbital formulas.
4. Dual velocity closure: escape-fall velocity invariant.
5. Finite horizon values.
6. Light travel time correction.
7. Energy condition diagnostics proxy.

© 2025 Carmen Wrede & Lino Casu
Licensed under the Anti-Capitalist Software License v1.4
"""

import pytest
import numpy as np
from math import isclose
from ssz_metric_pure.constants import C, G, M_SUN, PHI
from ssz_metric_pure.core import characteristic_radius
from ssz_metric_pure.observable_predictions import (
    predict_time_dilation,
    predict_redshift,
    predict_light_travel_time_correction,
    predict_lensing_ppn,
    predict_shapiro_ppn,
    predict_perihelion_ppn,
    predict_dual_velocity_product,
    predict_finite_horizon_values,
    predict_energy_condition_diagnostic
)


def test_gps_time_dilation_clocks():
    """Verify time dilation routing and calculations using direct D(r) path."""
    # Orbit radius of GPS satellite
    r = 2.656e7
    M = 5.972e24
    dilation = predict_time_dilation(r, M)
    assert dilation > 0.0
    # Expected approximate Earth surface-to-orbit dilation rate difference (GR order of magnitude)
    assert dilation < 1.0e-8


def test_redshift_predictions():
    """Verify frequency redshift calculations using explicit D ratio and sign convention."""
    r_emit = 6378100.0
    r_obs = 6378122.5  # 22.5m elevation (Pound-Rebka)
    M = 5.972e24
    z = predict_redshift(r_emit, r_obs, M)
    # Gravitational redshift from emitter to observer: z should be positive for outwards frequency shift
    assert z > 0.0
    assert isclose(z, 2.44e-15, rel_tol=1e-2)


def test_lensing_deflection():
    """Verify Eddington lensing deflection routing under PPN completion (1+gamma)."""
    r_s = characteristic_radius(M_SUN)
    b = 696340000.0  # Solar radius
    
    # Under PPN completion, gamma_ppn = 1.0 implies factor of 2
    angle = predict_lensing_ppn(r_s, b, gamma_ppn=1.0)
    expected_angle = 2.0 * r_s / b
    assert isclose(angle, expected_angle, rel_tol=1e-12)
    assert isclose(angle, 8.4834e-6, rel_tol=1e-3)


def test_shapiro_delay():
    """Verify Shapiro time delay PPN completion (1+gamma) and docstring note."""
    r_s = characteristic_radius(M_SUN)
    r1 = 1.496e11
    r2 = 1.433e12
    d = 1.391e9
    
    delay = predict_shapiro_ppn(r_s, r1, r2, d, gamma_ppn=1.0)
    assert delay > 0.0
    # Verify PPN scale factor of 2.0 is included in calculation
    expected = 2.0 * (r_s / C) * np.log(4.0 * r1 * r2 / (d ** 2))
    assert isclose(delay, expected, rel_tol=1e-12)


def test_perihelion_orbit_precession():
    """Verify perihelion precession does not use a Xi-only shortcut."""
    M = 1.989e30
    a = 5.791e10
    e = 0.2056
    
    precession = predict_perihelion_ppn(M, a, e)
    # Value must correspond to exact standard PPN orbit formula
    expected = 3.0 * np.pi * characteristic_radius(M) / (a * (1.0 - e**2))
    assert isclose(precession, expected, rel_tol=1e-12)


def test_dual_velocity_invariant():
    """Verify the escape-fall dual velocity invariant holds exactly."""
    r = 1.0e7
    M = 5.972e24
    product = predict_dual_velocity_product(r, M)
    assert isclose(product, C ** 2, rel_tol=1e-12)


def test_finite_horizon():
    """Verify regularized finite dilation D at r = r_s."""
    r_s = characteristic_radius(M_SUN)
    D_horizon = predict_finite_horizon_values(M_SUN)
    
    # Xi_strong(r_s) = 1 - e^-phi
    # D = 1 / (1 + Xi_strong(r_s)) = 1 / (2 - e^-phi)
    expected_xi = 1.0 - np.exp(-PHI)
    expected_D = 1.0 / (1.0 + expected_xi)
    assert isclose(D_horizon, expected_D, rel_tol=1e-12)
    assert D_horizon > 0.5


def test_light_travel_time_radial_correction():
    """Verify radial light travel time correction is positive and monotonic."""
    M = 5.972e24
    # From r1 to r2
    dt1 = predict_light_travel_time_correction(1e7, 2e7, M)
    dt2 = predict_light_travel_time_correction(1e7, 3e7, M)
    
    assert dt1 > 0.0
    assert dt2 > dt1


def test_energy_condition_diagnostics_proxy():
    """Verify energy condition diagnostics are scoped as proxy check."""
    M = 1.989e30
    # Inside regularized NS domain
    diag = predict_energy_condition_diagnostic(20000.0, M)
    assert diag == 1.0
    
    # Check coords tuple version
    diag_coords = predict_energy_condition_diagnostic((0.0, 20000.0, 0.5, 0.0), M)
    assert diag_coords == 1.0
