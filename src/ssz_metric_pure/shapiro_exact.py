"""
SSZ Shapiro Delay - Exact Analytical Implementation

Following Segmented Spacetime with the metric
    ds^2 = -c^2 dt^2 / (1+Xi)^2 + (1+Xi)^2 dr^2 + r^2 dOmega^2,
a RADIAL NULL ray requires dt/dr = (1+Xi)^2 / c. Hence the extra travel time
relative to a flat radial reference of the same coordinate extent is
    Delta t = (1/c) integral[ (1+Xi)^2 - 1 ] dr = (1/c) integral (2 Xi + Xi^2) dr.

For the weak-field branch (r/r_s > 2.2):
Xi(r) = r_s / (2r);  s(r) = 1 + r_s/(2r)
Exact integral: integral[(1+Xi)^2 - 1] dr = r_s ln(r) - r_s^2/(4r) + C

[REPAIR 2026-10-13, forensic audit Phase D1: previous version integrated
(1 + Xi) dr instead of ((1+Xi)^2 - 1) dr, i.e. it dropped the leading 2*Xi term
and reported ~(1/2) of the metric-implied delay. Root cause: docstring conflated
the radial scale factor s(r) with the metric time integrand.]

© 2026 Carmen N. Wrede & Lino Casu
Licensed under the Anti-Capitalist Software License v1.4
"""

import numpy as np
from .constants import C
from .core import xi_canonical, s_from_xi, characteristic_radius


def shapiro_delay_weak_field_exact(r1, r2, mass):
    """
    Exact analytical Shapiro delay for weak-field SSZ (radial null ray).

    Extra time vs flat reference: (1/c) * integral[(1+Xi)^2 - 1] dr
    with Xi = r_s/(2r):  = (1/c) * [ r_s*ln(r2/r1) - r_s^2/4*(1/r2 - 1/r1) ]

    Args:
        r1: Start radius (m)
        r2: End radius (m)
        mass: Central mass (kg)

    Returns:
        Shapiro delay in seconds (exact analytical)
    """
    r_s = characteristic_radius(mass)

    # Exact analytical integral of (2*Xi + Xi^2) for Xi = r_s/(2r):
    # 2*Xi + Xi^2 = r_s/r + r_s^2/(4 r^2)
    # integral dr = r_s*ln(r) - r_s^2/(4 r)
    integral = r_s * np.log(r2 / r1) - (r_s**2 / 4.0) * (1.0/r2 - 1.0/r1)

    return float(integral / C)


def shapiro_delay_numerical_exact(r1, r2, mass, n_points=10000):
    """
    Exact numerical Shapiro delay for full SSZ (all regimes).
    
    Uses exact SSZ metric with piecewise Ξ(r):
    - Strong: Ξ = 1 - exp(-φ * r_s/r)
    - Blend: Hermite C² interpolation
    - Weak: Ξ = r_s / (2r)
    
    Args:
        r1: Start radius (m)
        r2: End radius (m)
        mass: Central mass (kg)
        n_points: Integration resolution
        
    Returns:
        Shapiro delay in seconds (exact numerical)
    """
    rs = np.linspace(r1, r2, n_points)
    dt_total = 0.0
    
    for i in range(n_points - 1):
        dr = rs[i+1] - rs[i]
        r_mid = (rs[i] + rs[i+1]) / 2
        
        # Exact SSZ scale factor s(r) = 1 + Ξ(r)
        xi = xi_canonical(r_mid, mass)
        s = s_from_xi(xi)
        
        # Null-ray metric integrand: dt/dr = s^2/c -> extra time factor (s^2 - 1) = 2*Xi + Xi^2.
        # [REPAIR 2026-10-13, forensic audit Phase D1: previous code accumulated s*dr/c and
        # labeled it "Proper time increment ds" — that is the coordinate time of the metric
        # (correct as total time) but the subtraction of geometric_time then yields
        # integral(s-1)dr/c = integral(Xi)dr/c, missing the Xi^2 term; the true excess over
        # the flat reference is integral((1+Xi)^2-1)dr/c. Fixed by accumulating s^2.]
        dt_total += s * s * dr / C
    
    # Subtract geometric time to get delay
    geometric_time = (r2 - r1) / C
    delay = dt_total - geometric_time
    
    return float(delay)


def shapiro_delay_full(r_emitter, r_receiver, mass, b_impact=None):
    """
    Complete SSZ Shapiro delay calculation.
    
    Uses exact analytical solution where valid,
    numerical integration for complex paths.
    
    Args:
        r_emitter: Emitter radial coordinate (m)
        r_receiver: Receiver radial coordinate (m)
        mass: Central mass (kg)
        b_impact: Impact parameter (m), defaults to min radius
        
    Returns:
        dict with {
            'delay_seconds': Shapiro delay in seconds,
            'delay_microseconds': delay in microseconds,
            'method': 'analytical' or 'numerical',
            'regime': 'strong', 'blend', 'weak', or 'mixed'
        }
    """
    if b_impact is None:
        b_impact = min(r_emitter, r_receiver)
    
    r_s = characteristic_radius(mass)
    
    # Determine regime
    x_emitter = r_emitter / r_s
    x_receiver = r_receiver / r_s
    x_impact = b_impact / r_s
    
    if x_emitter > 2.2 and x_receiver > 2.2 and x_impact > 2.2:
        # Pure weak-field: use exact analytical
        delay = shapiro_delay_weak_field_exact(r_emitter, r_receiver, mass)
        method = 'analytical'
        regime = 'weak'
    else:
        # Mixed or strong: use numerical exact
        delay = shapiro_delay_numerical_exact(r_emitter, r_receiver, mass)
        method = 'numerical'
        if x_impact < 1.8:
            regime = 'strong'
        elif x_impact < 2.2:
            regime = 'blend'
        else:
            regime = 'mixed'
    
    return {
        'delay_seconds': delay,
        'delay_microseconds': delay * 1e6,
        'method': method,
        'regime': regime,
        'r_s': r_s,
        'impact_parameter': b_impact
    }


__all__ = [
    'shapiro_delay_weak_field_exact',
    'shapiro_delay_numerical_exact', 
    'shapiro_delay_full'
]
