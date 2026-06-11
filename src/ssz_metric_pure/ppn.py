"""
SSZ Parameterized Post-Newtonian (PPN) Module

Evaluates weak field PPN expansion coefficients for Segmented Spacetime.
For canonical SSZ, we recover standard GR limits in the weak field:
    beta_PPN = 1.0
    gamma_PPN = 1.0

© 2025 Carmen Wrede & Lino Casu
Licensed under the Anti-Capitalist Software License v1.4
"""

import numpy as np
from .constants import C
from .core import xi_weak, characteristic_radius


def beta_ppn_parameter() -> float:
    """
    Returns the PPN beta parameter (non-linear metric self-coupling).
    For canonical SSZ, beta_PPN = 1.0 identically.
    """
    return 1.0


def gamma_ppn_parameter() -> float:
    """
    Returns the PPN gamma parameter (space curvature per unit mass).
    For canonical SSZ, gamma_PPN = 1.0 identically.
    """
    return 1.0


def ppn_gamma() -> float:
    """
    Alias for gamma_ppn_parameter.
    """
    return gamma_ppn_parameter()


def ppn_beta() -> float:
    """
    Alias for beta_ppn_parameter.
    """
    return beta_ppn_parameter()


def lensing_deflection_ppn(r_s: float, b: float, gamma_ppn: float = 1.0) -> float:
    """
    Predict first-order light deflection angle under PPN completion.
    alpha = (1 + gamma_ppn) * r_s / b
    """
    return float((1.0 + gamma_ppn) * r_s / b)


def shapiro_delay_ppn(r_s: float, r1: float, r2: float, d: float, gamma_ppn: float = 1.0) -> float:
    """
    Predict Shapiro time delay under PPN completion.
    delta_t = (1 + gamma_ppn) * (r_s / C) * log(4 * r1 * r2 / d^2)
    """
    val = (4.0 * r1 * r2) / (d ** 2)
    return float((1.0 + gamma_ppn) * (r_s / C) * np.log(val))


def perihelion_precession_ppn(M: float, a: float, e: float) -> float:
    """
    Predict perihelion precession rate per orbit under PPN orbit formulation.
    delta_omega = 6 * pi * G * M / (a * (1 - e^2) * c^2)
    """
    r_s = characteristic_radius(M)
    val = 3.0 * np.pi * r_s / (a * (1.0 - e**2))
    return float(val)


def weak_field_expansion_coeffs(r: float, M: float) -> dict:
    """
    Generate PPN-style weak field expansion coefficients for the metric.
    In the weak field, Xi = r_s / (2r) = U(r).
    Therefore:
        g_tt ≈ -(1 - 2U + 2U²) c²
        g_rr ≈ 1 + 2U + 3U²
    """
    r_s = characteristic_radius(M)
    U = r_s / (2.0 * r)
    
    return {
        "U": U,
        "g_tt_coeff_order1": -2.0,
        "g_tt_coeff_order2": 2.0,
        "g_rr_coeff_order1": 2.0,
        "g_rr_coeff_order2": 3.0
    }
