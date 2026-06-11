"""
SSZ Kinematics Module

Implements particle and photon kinematics in the canonical Segmented Spacetime (SSZ) metric.
All kinematical quantities are derived strictly from the primary segment density field Xi(r).

© 2025 Carmen N. Wrede & Lino Casu
Licensed under the Anti-Capitalist Software License v1.4
"""

import numpy as np
from .constants import C
from .core import xi_canonical, D_from_xi, s_from_xi, gamma_from_xi, beta_from_gamma


def coordinate_light_speed(r: float, M: float) -> float:
    """
    Calculate the radial coordinate speed of light dr/dT.
    Formula:
        dr/dT = c * D(r) / s(r) = c * D(r)² = c / (1 + Xi(r))²
    """
    xi = xi_canonical(r, M)
    D = D_from_xi(xi)
    return C * (D ** 2)


def free_fall_velocity_profile(r: float, M: float, r_start: float) -> float:
    """
    Compute radial velocity for a particle in free fall starting from rest at r_start.
    Based on the conservation of energy under the diagonal SSZ metric.
    """
    xi_start = xi_canonical(r_start, M)
    xi_current = xi_canonical(r, M)
    
    D_start = D_from_xi(xi_start)
    D_current = D_from_xi(xi_current)
    s_current = s_from_xi(xi_current)
    
    # Conservation of energy: D(r) * dt/dtau = E / m = D(r_start) / D(r_start) = 1 (if starting from rest)
    # Yields: v = dr/dT = D(r) * sqrt(1 - (D(r)/D(r_start))²) / s(r)
    ratio = D_current / D_start
    if ratio >= 1.0:
        return 0.0
    return D_current * np.sqrt(1.0 - ratio ** 2) / s_current


def v_fall(r: float, M: float) -> float:
    """
    Compute fall velocity from infinity: v_fall = c * beta.
    """
    xi = xi_canonical(r, M)
    gamma = gamma_from_xi(xi)
    beta = beta_from_gamma(gamma)
    return C * beta


def v_escape(r: float, M: float) -> float:
    """
    Compute escape velocity: v_escape = c / beta.
    """
    xi = xi_canonical(r, M)
    gamma = gamma_from_xi(xi)
    beta = beta_from_gamma(gamma)
    return C / beta if beta > 0 else float("inf")


def dual_velocity_product(r: float, M: float) -> float:
    """
    Compute the dual velocity product: v_fall * v_escape.
    Axiom: v_fall * v_escape = c^2 identically.
    """
    vf = v_fall(r, M)
    ve = v_escape(r, M)
    return vf * ve
