"""
SSZ Blend Zone - Hermite C² Interpolation

Implements the canonical blend zone between weak and strong field regimes
using quintic Hermite interpolation for C² continuity.

Source: SSZ-HOW-TO-BEAM/src/beam_ssz/xi.py
"""

import numpy as np
from typing import Tuple
from .constants import PHI, X_BLEND_MIN, X_BLEND_MAX

def _compute_hermite_coeffs():
    """
    Compute Hermite C² coefficients ensuring continuity at blend boundaries.
    
    Boundary conditions:
    - At x=1.8 (strong): Ξ = 1-exp(-PHI/1.8), dΞ/dx = (PHI/1.8²)*exp(-PHI/1.8)
    - At x=2.2 (weak): Ξ = 1/(2*2.2), dΞ/dx = -1/(2*2.2²)
    """
    # Values at boundaries
    xi_18 = 1.0 - np.exp(-PHI / 1.8)  # ~0.592986
    xi_22 = 1.0 / (2.0 * 2.2)         # ~0.227273
    
    # Derivatives at boundaries (with respect to x = r/r_s)
    dxi_18 = (PHI / 1.8**2) * np.exp(-PHI / 1.8)  # ~0.329876
    dxi_22 = -1.0 / (2.0 * 2.2**2)                  # ~-0.103306
    
    # Convert to t-parameter space (t=0 at x=1.8, t=1 at x=2.2)
    dx = 2.2 - 1.8  # 0.4
    
    # Hermite quintic coefficients for C² continuity
    # H(t) = a0 + a1*t + a2*t² + a3*t³ + a4*t⁴ + a5*t⁵
    # Conditions: H(0)=xi_18, H(1)=xi_22, H'(0)=dxi_18*dx, H'(1)=dxi_22*dx
    # For C²: H''(0)=0, H''(1)=0 (natural boundary)
    
    a0 = xi_18
    a1 = dxi_18 * dx
    a2 = 0.0  # C²: second derivative = 0 at t=0
    
    # Solve for a3, a4, a5 using boundary conditions at t=1
    # H(1) = xi_22
    # H'(1) = dxi_22 * dx  
    # H''(1) = 0
    
    # This gives the system:
    # a0 + a1 + a2 + a3 + a4 + a5 = xi_22
    # a1 + 2*a2 + 3*a3 + 4*a4 + 5*a5 = dxi_22 * dx
    # 2*a2 + 6*a3 + 12*a4 + 20*a5 = 0
    
    # With a2=0:
    # a3 + a4 + a5 = xi_22 - a0 - a1
    # 3*a3 + 4*a4 + 5*a5 = dxi_22*dx - a1
    # 6*a3 + 12*a4 + 20*a5 = 0
    
    b1 = xi_22 - a0 - a1
    b2 = dxi_22 * dx - a1
    b3 = 0.0
    
    # Solve 3x3 system
    A = np.array([[1, 1, 1], [3, 4, 5], [6, 12, 20]], dtype=float)
    b = np.array([b1, b2, b3], dtype=float)
    coeffs = np.linalg.solve(A, b)
    
    return (a0, a1, a2, coeffs[0], coeffs[1], coeffs[2])

# Compute coefficients at module load time
_HERMITE_COEFFS = _compute_hermite_coeffs()


def Xi_strong_raw(r: float, r_s: float) -> float:
    """Strong field Xi (decay form) - raw formula."""
    x = r / r_s
    return 1.0 - np.exp(-PHI / x)


def Xi_weak_raw(r: float, r_s: float) -> float:
    """Weak field Xi - raw formula."""
    x = r / r_s
    return 1.0 / (2.0 * x)


def dXi_strong_raw(r: float, r_s: float) -> float:
    """Derivative of strong field Xi."""
    x = r / r_s
    return -(PHI / x**2) * np.exp(-PHI / x) / r_s


def dXi_weak_raw(r: float, r_s: float) -> float:
    """Derivative of weak field Xi."""
    x = r / r_s
    return -1.0 / (2.0 * x**2 * r_s)


def Xi_blend(r: float, r_s: float) -> Tuple[float, float, float]:
    """
    Blend zone with Hermite C² interpolation.
    
    Returns:
        (xi, dxi_dr, d2xi_dr2) - value and derivatives
    """
    x = r / r_s
    
    if not (X_BLEND_MIN <= x <= X_BLEND_MAX):
        raise ValueError(f"Blend only valid for {X_BLEND_MIN} <= r/r_s <= {X_BLEND_MAX}")
    
    dx = X_BLEND_MAX - X_BLEND_MIN
    t = (x - X_BLEND_MIN) / dx
    
    a0, a1, a2, a3, a4, a5 = _HERMITE_COEFFS
    
    # Hermite polynomial evaluation
    xi = a0 + a1*t + a2*t**2 + a3*t**3 + a4*t**4 + a5*t**5
    
    # First derivative (with respect to t)
    dxi_dt = a1 + 2*a2*t + 3*a3*t**2 + 4*a4*t**3 + 5*a5*t**4
    dxi_dr = dxi_dt / (dx * r_s)
    
    # Second derivative
    d2xi_dt2 = 2*a2 + 6*a3*t + 12*a4*t**2 + 20*a5*t**3
    d2xi_dr2 = d2xi_dt2 / (dx * r_s)**2
    
    return xi, dxi_dr, d2xi_dr2


def Xi_complete(r: float, r_s: float) -> Tuple[float, float, float]:
    """
    Complete Xi evaluation with automatic regime detection.
    
    Returns:
        (xi, dxi_dr, d2xi_dr2) - value and derivatives
    """
    x = r / r_s
    
    if x < X_BLEND_MIN:
        # Strong field
        xi = Xi_strong_raw(r, r_s)
        dxi = dXi_strong_raw(r, r_s)
        # Numerical second derivative
        eps = 1e-8
        dxi_plus = dXi_strong_raw(r + eps, r_s)
        dxi_minus = dXi_strong_raw(r - eps, r_s)
        d2xi = (dxi_plus - dxi_minus) / (2 * eps)
        return xi, dxi, d2xi
        
    elif x <= X_BLEND_MAX:
        # Blend zone - Hermite C²
        return Xi_blend(r, r_s)
        
    else:
        # Weak field
        xi = Xi_weak_raw(r, r_s)
        dxi = dXi_weak_raw(r, r_s)
        # Numerical second derivative
        eps = 1e-8
        dxi_plus = dXi_weak_raw(r + eps, r_s)
        dxi_minus = dXi_weak_raw(r - eps, r_s)
        d2xi = (dxi_plus - dxi_minus) / (2 * eps)
        return xi, dxi, d2xi


def dXi_blend_dr(r: float, r_s: float) -> float:
    """First derivative of blend zone Xi."""
    _, dxi, _ = Xi_blend(r, r_s)
    return dxi
