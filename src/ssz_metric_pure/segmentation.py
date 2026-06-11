"""
SSZ Physical Segmentation and Orthonormal Invariance Module

This module implements the core operational metrics and observables of Segmented Spacetime:
1. Operational segment density field Xi(r)
2. Operational segment scaling s(r)
3. Operational segment distance integration dρ = s(r) dr
4. Segment count proxies
5. Orthonormal frame light-speed invariance (local c invariance)

© 2025 Carmen Wrede & Lino Casu
Licensed under the Anti-Capitalist Software License v1.4
"""

import numpy as np
from .constants import G, C
from .core import xi_canonical, s_from_xi, D_from_xi, ArrayLike


def segment_density(r: ArrayLike, M: float) -> ArrayLike:
    """
    Primary physical Segment Density field Xi(r).
    """
    return xi_canonical(r, M)


def segment_scale(r: ArrayLike, M: float) -> ArrayLike:
    """
    Radial segment stretching factor s(r) = 1 + Xi(r).
    """
    xi = segment_density(r, M)
    return s_from_xi(xi)


def segment_distance(r1: float, r2: float, M: float, n: int = 10000) -> float:
    """
    Compute the operational segment distance between coordinate radii r1 and r2.
    Formula:
        ρ(r1, r2) = ∫_{r1}^{r2} s(r) dr
    """
    if r1 > r2:
        r1, r2 = r2, r1
        
    r_vals = np.linspace(r1, r2, n)
    s_vals = segment_scale(r_vals, M)
    
    # Perform numerical integration using the trapezoidal rule
    return float(np.trapezoid(s_vals, r_vals))


def segment_count_proxy(r1: float, r2: float, M: float, ell0: float = 1.0) -> float:
    """
    Compute the effective segment count between coordinate radii r1 and r2.
    Formula:
        Count = ρ(r1, r2) / ell0
    """
    return segment_distance(r1, r2, M) / ell0


def local_orthonormal_speed_check(r: float, M: float) -> float:
    """
    Verify local speed-of-light invariance in a local orthonormal frame.
    For a radial null geodesic:
        ds² = 0 = -D(r)² c² dT² + s(r)² dr²
    Therefore:
        d r_hat = s(r) dr
        d t_hat = D(r) dT
    And:
        d r_hat / d t_hat = [s(r) dr] / [D(r) dT] = c
    
    This function computes the local orthonormal speed using the null geodesic condition:
        dr/dT = c * D(r) / s(r)
    And evaluates:
        Local Speed = s(r) * (dr/dT) / D(r) == c identically!
    """
    xi = xi_canonical(r, M)
    D = D_from_xi(xi)
    s = s_from_xi(xi)
    
    # Coordinate speed of light dr/dT
    coord_speed = C * D / s
    
    # Local orthonormal speed = s * (dr/dT) / D
    local_speed = s * coord_speed / D
    return float(local_speed)
