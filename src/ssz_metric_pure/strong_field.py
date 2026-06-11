"""
SSZ Strong Field Module

Implements strong-field structure and photon-sphere dynamics under canonical SSZ.

© 2025 Carmen Wrede & Lino Casu
Licensed under the Anti-Capitalist Software License v1.4
"""

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
