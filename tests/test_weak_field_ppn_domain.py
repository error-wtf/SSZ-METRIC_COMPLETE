"""
Tests for the SSZ Weak-Field PPN Scale Domain.

© 2025 Carmen N. Wrede & Lino Casu
Licensed under the Anti-Capitalist Software License v1.4
"""

import pytest
import numpy as np
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
    """Verify the metric-derived PPN parameters of the SSZ weak-field branch.

    FORENSIC AUDIT (2026-10-13): the old assertions (gamma == 1.0 and
    beta == 1.0) hardcoded GR values that the ORIGINAL code could never
    produce: ppn.py contained a literal `return 1.0 / 1.0` hardcode. The
    metric-derived values are (sympy-exact, Lambert-W isotropic inversion
    rho = r e^{-1/2r}):

        -g_tt/c^2 = 1 - 1/rho + 5/(4 rho^2) - 13/(8 rho^3)  -> beta = 5/2
        g_rr^iso   = 1 + 1/rho + 1/(24 rho^3)               -> gamma = 1

    Numerically (deg-4 fit on the uniform 1/rho grid): beta = 2.499964,
    gamma = 0.999950. These are METRIC PROPERTIES, not bugs.
    """
    gamma = ppn_gamma()
    beta = ppn_beta()
    print(f"  PPN gamma = {gamma} (expected: 1 + O(1e-5) fit truncation)")
    print(f"  PPN beta = {beta} (expected: 5/2 = 2.5, metric property)")
    assert isclose(gamma, 1.0, abs_tol=1e-4)
    assert isclose(beta, 2.5, abs_tol=1e-4)


def test_lensing_and_shapiro_completion():
    """Verify that light deflection and Shapiro delays implement PPN completion factors of (1+gamma)."""
    r_s = characteristic_radius(M_SUN)
    b = 696340000.0  # Solar radius

    angle = lensing_deflection_ppn(r_s, b, gamma_ppn=1.0)
    expected_angle = 2.0 * r_s / b
    angle_arcsec = angle * (180/np.pi) * 3600

    print(f"  Lensing deflection: {angle_arcsec:.4f} arcsec")
    print(f"  Expected (PPN, 1+gamma=2): {angle:.6e} rad")
    print(f"  PPN factor: 2.0")

    assert isclose(angle, expected_angle, rel_tol=1e-12)

    # Shapiro delay
    r1 = 1.496e11
    r2 = 1.433e12
    d = 1.391e9
    delay = shapiro_delay_ppn(r_s, r1, r2, d, gamma_ppn=1.0)
    # GR/PPN: Delta t = (1+gamma) GM/c^3 ln(4 r1 r2 / d^2) = (1+gamma) (r_s/2C) ln(...)
    # FORENSIC AUDIT: old test expected (1+gamma) r_s/C ln(...) — factor 2 too
    # large, matching the factor-2 bug that was in shapiro_delay_ppn itself.
    expected_delay = 2.0 * (r_s / (2.0 * C)) * np.log(4.0 * r1 * r2 / (d ** 2))
    assert isclose(delay, expected_delay, rel_tol=1e-12)


def test_perihelion_orbit_calculations():
    """Verify perihelion precession from the general PPN formula.

    General PPN: Delta omega = (2 + 2 gamma - beta) pi r_s / (a (1-e^2)).
    For SSZ (beta = 5/2, gamma = 1): (2 + 2 - 2.5) = 1.5 = 3/2 — exactly
    HALF the GR coefficient (3). The old test asserted the GR value with a
    hardcoded expected; the code now honestly reports the SSZ prediction.
    """
    # Sun mass, mercury semi-major, eccentricity
    M = 1.989e30
    a = 5.791e10
    e = 0.2056
    precession = perihelion_precession_ppn(M, a, e)
    r_s = characteristic_radius(M)
    # Use the SAME metric-derived fit values the routine uses (gamma, beta);
    # general PPN: Delta omega = 3 pi r_s/(a(1-e^2)) * (2+2 gamma - beta)/3.
    # For the exact SSZ metric (beta=5/2, gamma=1): coefficient 1.5 — half GR.
    gamma_v, beta_v = ppn_gamma(), ppn_beta()
    expected = 3.0 * np.pi * r_s / (a * (1.0 - e**2)) * (2.0 + 2.0 * gamma_v - beta_v) / 3.0

    print(f"  Mercury perihelion precession: {precession:.6e} rad/orbit")
    print(f"  Expected (SSZ PPN, (2+2gamma-beta)/3 with fit values): {expected:.6e} rad/orbit")
    print(f"  GR reference would be {3.0 * np.pi * r_s / (a * (1.0 - e**2)):.6e} (43 arcsec/century)")

    assert isclose(precession, expected, rel_tol=1e-12)
