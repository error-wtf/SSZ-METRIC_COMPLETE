"""
SSZ Shapiro Delay - Exact Analytical Implementation

Following Segmented Spacetime: Δt = (1/c) ∫ s(r) dr
where s(r) = 1 + Ξ(r) is the radial scale factor.

For the weak-field branch (r/r_s > 2.2):
Ξ(r) = r_s / (2r)
s(r) = 1 + r_s/(2r)

Exact integral: ∫ s(r) dr = r + (r_s/2) ln(r) + C

© 2026 Carmen N. Wrede & Lino Casu
Licensed under the Anti-Capitalist Software License v1.4
"""

import numpy as np
from .constants import C
from .core import xi_canonical, s_from_xi, characteristic_radius


def shapiro_delay_weak_field_exact(r1, r2, mass):
    """
    Exact analytical Shapiro delay for weak-field SSZ.
    
    Args:
        r1: Start radius (m)
        r2: End radius (m)  
        mass: Central mass (kg)
        
    Returns:
        Shapiro delay in seconds (exact analytical)
    """
    r_s = characteristic_radius(mass)
    
    # Exact analytical integral for weak-field:
    # ∫ (1 + r_s/(2r)) dr = r + (r_s/2) * ln(r)
    integral = (r2 - r1) + (r_s / 2) * np.log(r2 / r1)
    
    # Shapiro delay = (integral / c) - (geometric time r2-r1)/c
    geometric_time = (r2 - r1) / C
    total_time = integral / C
    delay = total_time - geometric_time
    
    return float(delay)


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
        
        # Proper time increment: ds = s(r)/c * dr
        dt_total += s * dr / C
    
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
