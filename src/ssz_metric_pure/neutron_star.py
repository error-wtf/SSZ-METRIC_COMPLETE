"""
SSZ Neutron Star Domain Module

Defines compactness, surface dilation, regime classification, and redshift predictions
characterizing neutron star scale systems in the static diagonal SSZ core.

© 2025 Carmen Wrede & Lino Casu
Licensed under the Anti-Capitalist Software License v1.4
"""

import numpy as np
from .core import xi_canonical, D_from_xi, characteristic_radius


def neutron_star_compactness(M: float, R: float) -> float:
    """
    Evaluate geometric compactness ratio r_s / R of a neutron star of mass M and radius R.
    """
    r_s = characteristic_radius(M)
    return float(r_s / R)


def neutron_star_regime(M: float, R: float) -> str:
    """
    Classify the surface regime of the neutron star based on its coordinate radius R.
    """
    r_s = characteristic_radius(M)
    x = R / r_s
    if x < 1.8:
        return "STRONG_FIELD_CORE_INTERNAL"
    elif x <= 2.2:
        return "BLEND_ZONE_TRANSITION"
    elif x <= 3.0:
        return "PHOTON_SPHERE_LIMIT"
    else:
        return "WEAK_FIELD_REGIME"


def neutron_star_redshift_prediction(M: float, R: float) -> float:
    """
    Predict gravitational redshift z at the surface of the neutron star:
    1 + z = 1 / D_surface = 1 + Xi(R)
    """
    xi_surf = xi_canonical(R, M)
    return float(xi_surf)


def neutron_star_surface_D(M: float, R: float) -> float:
    """
    Predict surface temporal dilation factor D(R) = 1 / (1 + Xi(R)).
    """
    xi_surf = xi_canonical(R, M)
    return float(D_from_xi(xi_surf))


def neutron_star_usecase_report(M: float, R: float) -> dict:
    """
    Generate a comprehensive scale domain report for a neutron star of mass M and radius R.
    Embeds honest limitations and caveats for astrophysical research.
    """
    return {
        "mass_kg": M,
        "radius_m": R,
        "geometric_compactness": neutron_star_compactness(M, R),
        "surface_regime": neutron_star_regime(M, R),
        "surface_redshift": neutron_star_redshift_prediction(M, R),
        "surface_dilation_D": neutron_star_surface_D(M, R),
        "fittings_allowed": False,
        "limitations": [
            "no full nuclear equation of state model",
            "no full rotating neutron-star model",
            "no full binary merger simulation",
            "no claim of complete observational proof",
            "this is a metric/regime/observable framework"
        ]
    }
