"""
SSZ Observable Predictions Module

Implements pure forward-calculating prediction functions for all observable domains
strictly derived from the canonical Xi-primary SSZ metric.

No curve fitting, parameter tuning, or post-hoc regression allowed here. All values
are evaluated forward from analytical definitions.

© 2025 Carmen N. Wrede & Lino Casu
Licensed under the Anti-Capitalist Software License v1.4
"""

import numpy as np
from .constants import C, G
from .core import xi_canonical, D_from_xi, s_from_xi, characteristic_radius
from .kinematics import coordinate_light_speed, dual_velocity_product
from .electromagnetism import light_travel_time_correction
from .energy import check_weak_energy_condition, check_strong_energy_condition


def predict_time_dilation(r: float, M: float) -> float:
    """
    Predict fractional time dilation rate compared to infinity using D(r).
    TIMELIKE_STATIC class, XI_DIRECT method.
    Formula:
        rate_diff = 1.0 - D(r) = 1.0 - 1 / (1 + Xi(r))
    """
    xi = xi_canonical(r, M)
    D = D_from_xi(xi)
    return float(1.0 - D)


def predict_redshift(r_emit: float, r_obs: float, M: float) -> float:
    """
    Predict the gravitational redshift factor z between r_emit and r_obs.
    TIMELIKE_STATIC class, XI_DIRECT method.
    Redshift convention:
        1 + z = D(r_obs) / D(r_emit) = (1 + Xi(r_emit)) / (1 + Xi(r_obs))
    """
    xi_emit = xi_canonical(r_emit, M)
    xi_obs = xi_canonical(r_obs, M)
    D_emit = D_from_xi(xi_emit)
    D_obs = D_from_xi(xi_obs)
    z = (D_obs / D_emit) - 1.0
    return float(z)


def predict_light_travel_time_correction(r1: float, r2: float, M: float) -> float:
    """
    Predict radial gravity light travel time correction delta_t_grav.
    NULL_LIGHT class, PPN_COMPLETION method.
    Formula:
        delta_t_grav = integral_r1^r2 (Xi(r) dr) / c
    """
    return float(light_travel_time_correction(r1, r2, M))


def predict_lensing_ppn(r_s: float, b: float, gamma_ppn: float = 1.0) -> float:
    """
    Predict first-order light deflection angle under PPN completion.
    NULL_LIGHT class, PPN_COMPLETION method.
    Formula:
        alpha = (1 + gamma_ppn) * r_s / b
    """
    return float((1.0 + gamma_ppn) * r_s / b)


def predict_shapiro_ppn(r_s: float, r1: float, r2: float, d: float, gamma_ppn: float = 1.0) -> float:
    """
    Predict Shapiro time delay under PPN completion.
    NULL_LIGHT class, PPN_COMPLETION method.
    Assumes one-way travel (or round-trip distinction in docstring: round-trip is 2 * delta_t).
    Formula:
        delta_t = (1 + gamma_ppn) * (r_s / C) * log(4 * r1 * r2 / d^2)
    """
    val = (4.0 * r1 * r2) / (d ** 2)
    return float((1.0 + gamma_ppn) * (r_s / C) * np.log(val))


def predict_perihelion_ppn(M: float, a: float, e: float) -> float:
    """
    Predict perihelion precession rate per orbit under PPN orbit formulation.
    TIMELIKE_ORBIT class, PPN_ORBIT method.
    Formula:
        delta_omega = 6 * pi * G * M / (a * (1 - e^2) * c^2)
    """
    r_s = characteristic_radius(M)
    # 6 * pi * G * M / (a * (1 - e^2) * c^2) = 3 * pi * r_s / (a * (1 - e^2))
    val = 3.0 * np.pi * r_s / (a * (1.0 - e**2))
    return float(val)


def predict_dual_velocity_product(r: float, M: float) -> float:
    """
    Predict escape-fall dual velocity product.
    KINEMATIC_INVARIANT class, SSZ_KINEMATIC_IDENTITY method.
    Identity:
        v_escape * v_fall = c^2
    """
    return float(dual_velocity_product(r, M))


def predict_finite_horizon_values(M: float) -> float:
    """
    Predict finite limit of D at r = r_s.
    STRONG_FIELD_DIAGNOSTIC class, XI_STRONG_FIELD_DIAGNOSTIC method.
    At r = r_s:
        Xi = 1 - exp(-phi)
        D = 1 / (1 + Xi)
    """
    r_s = characteristic_radius(M)
    xi = xi_canonical(r_s, M)
    D = D_from_xi(xi)
    return float(D)


def predict_energy_condition_diagnostic(r, M: float) -> float:
    """
    Evaluates WEC and SEC within core as diagnostic/proxy indicator.
    STRONG_FIELD_DIAGNOSTIC class, XI_STRONG_FIELD_DIAGNOSTIC method.
    Returns 1.0 if both satisfied, 0.0 otherwise.
    """
    if isinstance(r, (list, tuple, np.ndarray)):
        # If coordinates are passed (t, r, theta, phi), extract r at index 1
        r_val = r[1]
    else:
        r_val = r
    
    wec = check_weak_energy_condition(r_val, M)
    sec = check_strong_energy_condition(r_val, M)
    return 1.0 if (wec and sec) else 0.0
