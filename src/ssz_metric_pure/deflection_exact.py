"""
SSZ Light Deflection - Exact 2D Null Geodesic Integration

Following Segmented Spacetime with exact metric:
g_tt = -c²/(1+Ξ)², g_rr = (1+Ξ)²

Null geodesic equation for impact parameter b:
d²x/dλ² + Γ^μ_νρ (dx^ν/dλ)(dx^ρ/dλ) = 0

With SSZ spherical symmetry, deflection reduces to:
α = 2 ∫[b,∞] (dφ/dr) dr - π

where dφ/dr comes from null geodesic constraint.

© 2026 Carmen N. Wrede & Lino Casu
Licensed under the Anti-Capitalist Software License v1.4
"""

import numpy as np
from .core import xi_canonical, s_from_xi, characteristic_radius


def deflection_weak_field_exact(b, mass):
    """
    Exact analytical deflection for weak-field SSZ.
    
    For weak field (Ξ << 1): α = 4GM/(c²b) = 2r_s/b
    
    Args:
        b: Impact parameter (m)
        mass: Central mass (kg)
        
    Returns:
        Deflection angle in radians (exact weak-field)
    """
    r_s = characteristic_radius(mass)
    return 2.0 * r_s / b


def deflection_numerical_exact(b, mass, r_max=None, n_points=10000):
    """
    Exact numerical deflection via 2D null geodesic integration.
    
    Solves null geodesic equation with full SSZ metric piecewise:
    - Strong: Ξ = 1 - exp(-φ * r_s/r)
    - Blend: Hermite C²
    - Weak: Ξ = r_s/(2r)
    
    Args:
        b: Impact parameter (m)
        mass: Central mass (kg)
        r_max: Maximum integration radius (m), defaults to 1e6 * r_s
        n_points: Integration resolution
        
    Returns:
        Deflection angle in radians (exact numerical)
    """
    if r_max is None:
        r_max = 1e6 * characteristic_radius(mass)
    
    # Integration from closest approach (b) to infinity (r_max)
    # Null geodesic in SSZ: conserved quantity E = (c²/(1+Ξ)²) * dt/dλ
    # At closest approach b: angular momentum L = E * b * (1+Ξ(b))
    
    # Deflection integral:
    # α = π - 2 ∫[b,∞] (b/r²) / sqrt(1/s² - b²/r²) dr
    # where s = 1 + Ξ
    
    rs = np.linspace(b, r_max, n_points)
    dr = rs[1] - rs[0]
    
    integral = 0.0
    for i in range(1, n_points):
        r = rs[i]
        
        # SSZ scale factor at this radius
        xi = xi_canonical(r, mass)
        s = s_from_xi(xi)
        
        # Null geodesic integrand
        # dφ/dr = b / (r² * sqrt(1 - b²s²/r²))
        # But in SSZ with g_rr = s², we have effective potential
        
        term = (b / r**2) / np.sqrt(1/s**2 - b**2/r**2)
        integral += term * dr
    
    # Deflection: total angle minus π (straight line)
    alpha = 2 * integral - np.pi
    
    return float(alpha)


def deflection_full(b, mass, method='auto'):
    """
    Complete SSZ light deflection calculation.
    
    Args:
        b: Impact parameter (m)
        mass: Central mass (kg)
        method: 'analytical', 'numerical', or 'auto' (chooses best)
        
    Returns:
        dict with {
            'deflection_rad': deflection angle in radians,
            'deflection_arcsec': deflection in arcseconds,
            'method': 'analytical' or 'numerical',
            'regime': 'strong', 'blend', or 'weak',
            'impact_parameter': b,
            'r_s': characteristic radius
        }
    """
    r_s = characteristic_radius(mass)
    x = b / r_s
    
    # Determine regime
    if x < 1.8:
        regime = 'strong'
    elif x < 2.2:
        regime = 'blend'
    else:
        regime = 'weak'
    
    # Choose method
    if method == 'auto':
        if regime == 'weak' and x > 10:
            method = 'analytical'
        else:
            method = 'numerical'
    
    # Calculate
    if method == 'analytical':
        alpha_rad = deflection_weak_field_exact(b, mass)
    else:
        alpha_rad = deflection_numerical_exact(b, mass)
    
    # Convert to arcseconds
    alpha_arcsec = alpha_rad * (180/np.pi) * 3600
    
    return {
        'deflection_rad': alpha_rad,
        'deflection_arcsec': alpha_arcsec,
        'method': method,
        'regime': regime,
        'impact_parameter': b,
        'r_s': r_s
    }


__all__ = [
    'deflection_weak_field_exact',
    'deflection_numerical_exact',
    'deflection_full'
]
