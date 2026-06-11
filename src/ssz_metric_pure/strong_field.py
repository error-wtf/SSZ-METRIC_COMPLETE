"""
SSZ Strong Field Module

Implements strong-field structure and photon-sphere dynamics under canonical SSZ.

© 2025 Carmen Wrede & Lino Casu
Licensed under the Anti-Capitalist Software License v1.4
"""

import numpy as np
from .core import xi_canonical, D_from_xi, s_from_xi, characteristic_radius


def photon_sphere_radius(M: float) -> float:
    """
    Get the characteristic coordinate radius of the photon sphere.
    For standard static metrics of this class, the photon sphere occurs at r = 3 * r_s / 2
    or r = 3 * r_s depending on coordinates. Under SSZ-Core, it is located at:
        r_photon = 3 * r_s
    where r_s is the characteristic radius.
    """
    return 3.0 * characteristic_radius(M)


def strong_field_redshift_limit(M: float) -> float:
    """
    Compute the maximum redshift factor at the core boundary (r = r_s).
    Under standard GR, redshift goes to infinity at r_s (black hole).
    Under SSZ, the core is regularized and has a finite limit:
        1 + z = 1 / D(r_s) = 1 + Xi(r_s) = 2 - exp(-phi) ≈ 1.8017118
    """
    r_s = characteristic_radius(M)
    xi_rs = xi_canonical(r_s, M)
    return float(1.0 + xi_rs)


def Xi_at_schwarzschild_radius(M: float) -> float:
    """
    Evaluate primary segment density field Xi(r) exactly at r = r_s.
    Axiomatic limit: Xi_strong(r_s) = 1 - exp(-phi) ≈ 0.8017118
    """
    r_s = characteristic_radius(M)
    return float(xi_canonical(r_s, M))


def Xi_at_characteristic_radius(M: float) -> float:
    """
    Alias for Xi_at_schwarzschild_radius.
    """
    return Xi_at_schwarzschild_radius(M)


def D_at_schwarzschild_radius(M: float) -> float:
    """
    Evaluate clock scaling factor D(r_s) exactly at r = r_s.
    D_at_r_s = 1 / (1 + Xi(r_s)) ≈ 1 / (2 - e^-phi) ≈ 0.55502
    """
    xi_rs = Xi_at_schwarzschild_radius(M)
    return float(D_from_xi(xi_rs))


def strong_field_regime_report(r: float, M: float) -> dict:
    """
    Generate a scale-domain regime report for radius r.
    Categorizes radial distance according to SSZ's physical boundaries.
    """
    r_s = characteristic_radius(M)
    x = r / r_s
    if x < 1.8:
        regime = "STRONG_FIELD_CORE"
    elif x <= 2.2:
        regime = "BLEND_ZONE"
    else:
        regime = "WEAK_FIELD"
    return {
        "radius": r,
        "x_compactness": x,
        "regime": regime,
        "xi": float(xi_canonical(r, M)),
        "D": float(D_from_xi(xi_canonical(r, M))),
        "s": float(s_from_xi(xi_canonical(r, M)))
    }


def compactness_report(R: float, M: float) -> dict:
    """
    Evaluate geometric compactness C_g = r_s / R of a static spherical boundary R.
    """
    r_s = characteristic_radius(M)
    return {
        "characteristic_radius": r_s,
        "boundary_radius": R,
        "compactness_ratio": r_s / R
    }


def finite_boundary_report(M: float) -> dict:
    """
    Provide boundary evaluation at characteristic radius r_s.
    """
    r_s = characteristic_radius(M)
    return {
        "r_s": r_s,
        "Xi_boundary": Xi_at_schwarzschild_radius(M),
        "D_boundary": D_at_schwarzschild_radius(M)
    }


def energy_condition_regime(coords, M: float) -> float:
    """
    Evaluates weak and strong energy conditions at coordinate location coords.
    Returns 1.0 if satisfied, 0.0 otherwise. Scoped as diagnostic proxy.
    """
    from .energy import check_weak_energy_condition, check_strong_energy_condition
    if isinstance(coords, (list, tuple, np.ndarray)):
        r = coords[1]
    else:
        r = coords
    wec = check_weak_energy_condition(r, M)
    sec = check_strong_energy_condition(r, M)
    return 1.0 if (wec and sec) else 0.0
