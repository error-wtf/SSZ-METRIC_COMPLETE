"""
SSZ Electromagnetic & Clock Observables Scale Module

Implements static gravitational time dilation, redshifts, GPS clock rate adjustments,
and electromagnetic field component scaling factors.

© 2025 Carmen Wrede & Lino Casu
Licensed under the Anti-Capitalist Software License v1.4
"""

import numpy as np
from .core import xi_canonical, D_from_xi, s_from_xi
from .electromagnetism import light_travel_time_correction as core_time_correction


def time_dilation_D(r: float, M: float) -> float:
    """
    Evaluate static dilation factor D(r) derived from Xi.
    """
    xi = xi_canonical(r, M)
    return float(D_from_xi(xi))


def redshift_static(r_emit: float, r_obs: float, M: float) -> float:
    """
    Evaluate gravitational static redshift:
    1 + z = D_obs / D_emit
    """
    D_emit = time_dilation_D(r_emit, M)
    D_obs = time_dilation_D(r_obs, M)
    return float((D_obs / D_emit) - 1.0)


def gps_clock_proxy(r_surface: float, r_orbit: float, M: float) -> float:
    """
    Proxy for net GPS clock correction rate difference between surface and orbit.
    """
    D_surf = time_dilation_D(r_surface, M)
    D_orb = time_dilation_D(r_orbit, M)
    return float((D_orb / D_surf) - 1.0)


def radial_scaling_factor(r: float, M: float) -> float:
    """
    Return spatial stretching scaling factor s(r).
    """
    xi = xi_canonical(r, M)
    return float(s_from_xi(xi))


def scale_electric_field(E: float, r: float, M: float) -> float:
    """
    Scale local electric field intensity component due to spatial segmentation:
    E_scaled = E * D(r)^2
    """
    xi = xi_canonical(r, M)
    D = D_from_xi(xi)
    return float(E * (D ** 2))


def scale_magnetic_field(B: float, r: float, M: float) -> float:
    """
    Scale local magnetic field intensity component:
    B_scaled = B * s(r)^2
    """
    xi = xi_canonical(r, M)
    s = s_from_xi(xi)
    return float(B * (s ** 2))


def light_travel_time_correction(r1: float, r2: float, M: float) -> float:
    """
    Calculate excess light travel time under canonical SSZ.
    """
    return float(core_time_correction(r1, r2, M))
