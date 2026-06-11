"""
SSZ Electromagnetism Module

Implements electromagnetic propagation properties and effective refractive index
in the canonical Segmented Spacetime (SSZ) metric.

© 2025 Carmen N. Wrede & Lino Casu
Licensed under the Anti-Capitalist Software License v1.4
"""

import numpy as np
from .constants import C
from .core import xi_canonical, D_from_xi, s_from_xi


def effective_refractive_index(r: float, M: float) -> float:
    """
    Compute the effective gravitational refractive index n(r) for light propagation.
    In the diagonal metric, the coordinate speed of light is dr/dT = c / n(r).
    Therefore:
        n(r) = s(r) / D(r) = (1 + Xi(r))²
    """
    xi = xi_canonical(r, M)
    s = s_from_xi(xi)
    D = D_from_xi(xi)
    return float(s / D)


def phase_velocity_ratio(r: float, M: float) -> float:
    """
    Calculate the ratio of local phase velocity to vacuum light speed: v_phase / c.
    Formula:
        v_phase / c = D(r) / s(r) = 1 / (1 + Xi(r))²
    """
    xi = xi_canonical(r, M)
    D = D_from_xi(xi)
    s = s_from_xi(xi)
    return float(D / s)


def light_travel_time_correction(r1: float, r2: float, M: float) -> float:
    """
    Compute light travel time correction delta_t_grav = integral_r1^r2 (Xi(r) dr) / c.
    Always positive for Xi > 0 and goes to zero as Xi -> 0.
    """
    if r1 > r2:
        r1, r2 = r2, r1
    r_vals = np.linspace(r1, r2, 500)
    xi_vals = xi_canonical(r_vals, M)
    return float(np.trapezoid(xi_vals, r_vals) / C)
