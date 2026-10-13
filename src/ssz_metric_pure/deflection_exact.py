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
    Exact weak-field SSZ deflection for closest approach b >> r_s:
    alpha -> (1 + gamma_PPN) * r_s / b with gamma_PPN = 1 for the weak branch,
    i.e. alpha = 2 r_s / b (standard leading order, metric-consistent).

    Args:
        b: Closest-approach radius (m)
        mass: Central mass (kg)

    Returns:
        Deflection angle in radians (leading order)
    """
    r_s = characteristic_radius(mass)
    return 2.0 * r_s / b


def deflection_numerical_exact(b, mass, r_max=None, n_points=10000):
    """
    Exact numerical deflection via radial null geodesic integral from the
    FULL metric ds^2 = -s^-2 c^2 dt^2 + s^2 dr^2 + r^2 dphi^2, s = 1 + Xi(r).

    Derivation (conserved E = s^-2 dt/dlambda, L = r^2 dphi/dlambda):
        0 = -s^-2 E^2 s^4... -> (dr/dlambda)^2 = E^2 (1/s^2... )
        dphi/dr = B / (r^2 sqrt(B_r (1/A_t - B^2/r^2)))  with  A_t = s^-2, B_r = s^2,
    i.e. dphi/dr = B / (r^2 sqrt(1 - B^2 s^2/r^2)) ... reduced form:
        dphi/dr = (B/r^2) / sqrt(s^-2 - B^2/r^2),  B = L/E.

    Turning point convention (forensic audit 2026-10-13): r0 = OUTERMOST root of
    the radicand 1/s^2 - B^2/r^2, found by scan + bisection; the asymptotic
    impact parameter B is then B = r0 * s(r0). Previously the code started the
    integral at r = b with radicand (1/s^2 - b^2/r^2) < 0 (negative at r = b
    because s(b) > 1), producing NaN/garbage for b near/inside 2.2 r_s.

    Args:
        b: Asymptotic impact parameter (m); turning point r0 found numerically
        mass: Central mass (kg)
        r_max: Outer integration radius (m), defaults to 1e6 * r_s
        n_points: Integration resolution (log-spaced)

    Returns:
        Deflection angle in radians
    """
    r_s = characteristic_radius(mass)
    if r_max is None:
        r_max = 1e6 * r_s

    radicand = lambda r: s_from_xi(xi_canonical(r, mass))**2 - (b * b) / (r * r)

    # 1) outermost (largest-r) root of the radicand via scan + bracketed bisection.
    #    CORRECT null-geodesic constraint (forensic audit): from the metric
    #    ds^2 = -c^2 dt^2/s^2 + s^2 dr^2 + r^2 dphi^2 with E = A_t dt/dlam,
    #    L = r^2 dphi/dlam one gets
    #        (dr/dlam)^2 = E^2/(A_t B_r) - L^2/(B_r r^2)
    #    -> turning point B^2 = r0^2 / A_t(r0) = r0^2 s(r0)^2  (r0 s(r0) = B)
    #    -> dphi/dr = (B s / r^2) / sqrt(s^2 - B^2/r^2).
    #    The PREVIOUS implementation used radicand 1/s^2 - b^2/r^2 (root at
    #    r = b*s instead of r*s = b) and integrand (b/r^2)/sqrt(1/s^2-b^2/r^2)
    #    — both wrong: it swapped the role of s between g_rr and the impact
    #    parameter, shifting the turning point and distorting the integrand.
    lo, hi = 1.001 * r_s, max(3.0 * b, 10.0 * r_s)
    grid = np.geomspace(lo, hi, 4000)
    rg_a = rg_b = None
    prev_r, prev_v = grid[0], radicand(grid[0])
    for rg in grid[1:]:
        cur = radicand(rg)
        if (prev_v > 0.0) != (cur > 0.0):        # sign change, either direction
            rg_a, rg_b = prev_r, rg
            break
        prev_r, prev_v = rg, cur
    if rg_a is None:
        # no root: no scattering orbit (ray plunges or escapes undeflected
        # in a regime without turning point)
        return float('inf')
    # bracketed bisection to the outermost root
    r_a, r_b = rg_a, rg_b
    for _ in range(200):
        mid = 0.5 * (r_a + r_b)
        if (radicand(mid) > 0.0) == (radicand(r_b) > 0.0):
            r_b = mid
        else:
            r_a = mid
    r0 = 0.5 * (r_a + r_b)

    # 2) integrate with r = r0 + t^2 substitution (removes the 1/sqrt(r-r0)
    #    singularity; integrand -> finite limit at t=0) + Gauss-Legendre per
    #    segment — the forensic-standard scheme validated in
    #    GLOBAL_FORENSIC_V1/deflection_reference.py. A midpoint trapezoid on a
    #    log grid underestimates the singular head by ~30% (observed: negative
    #    deflection), hence this replacement.
    nodes, weights = np.polynomial.legendre.leggauss(200)
    t_max = float(np.sqrt(r_max - r0))
    integ = 0.0
    for a_, b_ in [(0.0, 0.5), (0.5, 1.0), (1.0, 3.0), (3.0, 10.0),
                   (10.0, 100.0), (100.0, t_max)]:
        for i in range(len(nodes)):
            t = 0.5 * (b_ - a_) * nodes[i] + 0.5 * (a_ + b_)
            w = 0.5 * (b_ - a_) * weights[i]
            rr = r0 + t * t
            rad = radicand(rr)
            if rad <= 0.0:
                continue
            integ += w * (2.0 * t) * (b * float(s_from_xi(xi_canonical(rr, mass))) / rr**2) / np.sqrt(rad)

    return float(2.0 * integ - np.pi)


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
