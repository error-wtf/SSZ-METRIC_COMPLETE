"""
Tests for the SSZ Weak-Field PPN Scale Domain.

© 2025 Carmen Wrede & Lino Casu
Licensed under the Anti-Capitalist Software License v1.4
"""

import pytest
from math import isclose
from ssz_metric_pure.constants import M_SUN, C
from ssz_metric_pure.core import characteristic_radius
from ssz_metric_pure.ppn import (
    ppn_gamma,
    ppn_beta,
    lensing_deflection_ppn,
    shapiro_delay_ppn,
    perihelion_precession_ppn
)


def test_ppn_parameters():
    """Verify standard weak-field GR-equivalence parameter settings (beta=1, gamma=1)."""
    assert ppn_gamma() == 1.0
    assert ppn_beta() == 1.0


def test_lensing_and_shapiro_completion():
    """Verify that light deflection and Shapiro delays implement PPN completion factors of (1+gamma)."""
    r_s = characteristic_radius(M_SUN)
    b = 696340000.0  # Solar radius
    
    angle = lensing_deflection_ppn(r_s, b, gamma_ppn=1.0)
    expected_angle = 2.0 * r_s / b
    assert isclose(angle, expected_angle, rel_tol=1e-12)
    
    # Shapiro delay
    r1 = 1.496e11
    r2 = 1.433e12
    d = 1.391e9
    delay = shapiro_delay_ppn(r_s, r1, r2, d, gamma_ppn=1.0)
    expected_delay = 2.0 * (r_s / C) * np.log(4.0 * r1 * r2 / (d ** 2)) if 'np' in globals() else 0.0
    # Let's import numpy to verify it cleanly
    import numpy as np
    expected_delay = 2.0 * (r_s / C) * np.log(4.0 * r1 * r2 / (d ** 2))
    assert isclose(delay, expected_delay, rel_tol=1e-12)


def test_perihelion_orbit_calculations():
    """Verify that perihelion calculations are generated from standard orbital mechanics."""
    # Sun mass, mercury semi-major, eccentricity
    M = 1.989e30
    a = 5.791e10
    e = 0.2056
    precession = perihelion_precession_ppn(M, a, e)
    # Correct formula: 3 * pi * r_s / (a * (1 - e^2))
    expected = 3.0 * np.pi * characteristic_radius(M) / (a * (1.0 - e**2)) if 'np' in globals() else 0.0
    import numpy as np
    expected = 3.0 * np.pi * characteristic_radius(M) / (a * (1.0 - e**2))
    assert isclose(precession, expected, rel_tol=1e-12)
