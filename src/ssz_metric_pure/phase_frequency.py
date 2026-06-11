"""
SSZ Quantum Frequency & Phase Transport Scale Module

Defines nonlocal phase accumulation integrals, local c invariance, and clock rates
governing wavelength/frequency scaling.

© 2025 Carmen Wrede & Lino Casu
Licensed under the Anti-Capitalist Software License v1.4
"""

import numpy as np
from .constants import C
from .core import xi_canonical, D_from_xi, s_from_xi
from .segmentation import local_orthonormal_speed_check
from .frequency import clock_comparison_ratio


def local_c_invariance_check(r: float, M: float) -> float:
    """
    Verify local speed of light invariance check in orthonormal frame.
    Must always equal C identically.
    """
    return float(local_orthonormal_speed_check(r, M))


def frequency_ratio_from_D(r_emit: float, r_obs: float, M: float) -> float:
    """
    Evaluate frequency ratio f_obs / f_emit derived from time dilation D(r).
    f_obs / f_emit = D(r_emit) / D(r_obs) = (1 + Xi(r_obs)) / (1 + Xi(r_emit))
    """
    xi_emit = xi_canonical(r_emit, M)
    xi_obs = xi_canonical(r_obs, M)
    D_emit = D_from_xi(xi_emit)
    D_obs = D_from_xi(xi_obs)
    return float(D_emit / D_obs)


def wavelength_ratio_from_s(r_emit: float, r_obs: float, M: float) -> float:
    """
    Evaluate wavelength ratio lambda_obs / lambda_emit derived from spatial stretching s(r).
    Using local invariant speed C = lambda(r) * f(r):
        lambda_obs / lambda_emit = s(r_obs) / s(r_emit) = (1 + Xi(r_obs)) / (1 + Xi(r_emit))
    """
    xi_emit = xi_canonical(r_emit, M)
    xi_obs = xi_canonical(r_obs, M)
    s_emit = s_from_xi(xi_emit)
    s_obs = s_from_xi(xi_obs)
    return float(s_obs / s_emit)


def phase_path_integral(path: list, M: float) -> float:
    """
    Calculate wave phase propagation accumulation integral along a radial path segment.
    """
    r_vals = np.array(path)
    # n_index = s(r)/D(r) = (1 + Xi(r))^2
    xi_vals = xi_canonical(r_vals, M)
    n_vals = (1.0 + xi_vals) ** 2
    return float(np.trapezoid(n_vals, r_vals))


def frequency_curvature_proxy(r: float, M: float) -> float:
    """
    Evaluate frequency curvature proxy which scales with segment field derivatives.
    """
    xi = xi_canonical(r, M)
    # Structural derivative-adjacent proxy indicator
    return float(xi / (r ** 2))


def clock_ratio(r1: float, r2: float, M: float) -> float:
    """
    Evaluate clock rate comparison ratio between r1 and r2.
    """
    return float(clock_comparison_ratio(r1, r2, M))
