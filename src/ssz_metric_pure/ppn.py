"""
SSZ Parameterized Post-Newtonian (PPN) Module

Evaluates weak field PPN expansion coefficients for Segmented Spacetime.
For canonical SSZ, we recover standard GR limits in the weak field:
    beta_PPN = 1.0
    gamma_PPN = 1.0

© 2025 Carmen Wrede & Lino Casu
Licensed under the Anti-Capitalist Software License v1.4
"""

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
