"""
SSZ Core Mathematical Potential and Axiomatic Calibration Module

This module implements the canonical mathematical potentials, calibration functions,
and smooth transition blend zone representations of Segmented Spacetime (SSZ).

Axiomatic Foundation:
In Segmented Spacetime, the Segment Density Xi(r) is the primary physical field.
All scaling factors, rapidity factors, and metric components are derived directly
from the primary Segment Density Xi(r):
- Time dilation: D(r) = 1 / (1 + Xi(r))
- Radial stretching: s(r) = 1 + Xi(r)
- Lorentz factor: gamma(r) = 1 + Xi(r)
- Velocity field: beta(r) = sqrt(1 - D(r)²) = sqrt(Xi(r)*(2 + Xi(r))) / (1 + Xi(r))

All functions are NumPy-vectorized to support both float scalars and NumPy arrays.

© 2025 Carmen N. Wrede & Lino Casu
Licensed under the Anti-Capitalist Software License v1.4
"""

import numpy as np
from typing import Tuple, Union
from .constants import G, C, PHI, X_BLEND_MIN, X_BLEND_MAX

# Type alias for scalar or array values
ArrayLike = Union[float, np.ndarray]


# ============================================================================
# AXIOMATIC SSZ-CORE POTENTIALS & PRIMARY SEGMENT DENSITY FIELD
# ============================================================================

def characteristic_radius(M: float, G_CONST: float = G, c_CONST: float = C) -> float:
    """Calculate the characteristic Schwarzschild radius r_s = 2GM/c²."""
    return (2.0 * G_CONST * M) / (c_CONST ** 2)


def compactness_x(r: ArrayLike, M: float, G_CONST: float = G, c_CONST: float = C) -> ArrayLike:
    """Calculate the dimensionless compactness x = r / r_s."""
    r_arr = np.asarray(r, dtype=float)
    r_s = characteristic_radius(M, G_CONST, c_CONST)
    # Avoid division by zero
    r_s_safe = np.maximum(r_s, 1e-30)
    return r_arr / r_s_safe


def xi_weak(r: ArrayLike, M: float, G_CONST: float = G, c_CONST: float = C) -> ArrayLike:
    """
    Weak-field branch of Segment Density, valid for r/r_s > 2.2.
    Formula:
        Xi_weak(r) = r_s / (2r)
    """
    r_arr = np.asarray(r, dtype=float)
    r_safe = np.maximum(r_arr, 1e-30)
    r_s = characteristic_radius(M, G_CONST, c_CONST)
    return r_s / (2.0 * r_safe)


def xi_strong(r: ArrayLike, M: float, G_CONST: float = G, c_CONST: float = C) -> ArrayLike:
    """
    Strong-field / inner branch of Segment Density, valid for r_s/r < 1.8.
    Formula:
        Xi_strong(r) = 1 - exp(-phi * r_s / r)
    """
    r_arr = np.asarray(r, dtype=float)
    r_safe = np.maximum(r_arr, 1e-30)
    r_s = characteristic_radius(M, G_CONST, c_CONST)
    return 1.0 - np.exp(-PHI * r_s / r_safe)


def _compute_hermite_coeffs() -> Tuple[float, float, float, float, float, float]:
    """
    Compute Hermite C² coefficients ensuring exact continuity of values,
    first derivatives, and second derivatives at both blend boundaries.
    """
    x1 = X_BLEND_MIN
    x2 = X_BLEND_MAX
    dx = x2 - x1
    
    # 1. Boundary values
    v1 = 1.0 - np.exp(-PHI / x1)
    v2 = 1.0 / (2.0 * x2)
    
    # 2. First derivatives (with respect to x)
    d1 = -(PHI / (x1 ** 2)) * np.exp(-PHI / x1)
    d2 = -1.0 / (2.0 * (x2 ** 2))
    
    # 3. Second derivatives (with respect to x)
    dd1 = (PHI / (x1 ** 3)) * np.exp(-PHI / x1) * (2.0 - PHI / x1)
    dd2 = 1.0 / (x2 ** 3)
    
    # 4. Coefficients at t = 0 (using chain rule)
    c0 = v1
    c1 = d1 * dx
    c2 = 0.5 * dd1 * (dx ** 2)
    
    # 5. Boundary conditions at t = 1
    B0 = v2 - c0 - c1 - c2
    B1 = d2 * dx - c1 - 2.0 * c2
    B2 = dd2 * (dx ** 2) - 2.0 * c2
    
    # Solve 3x3 system:
    #   c3 +  c4 +  c5 = B0
    #  3c3 + 4c4 + 5c5 = B1
    #  6c3 +12c4 +20c5 = B2
    A = np.array([
        [1.0, 1.0, 1.0],
        [3.0, 4.0, 5.0],
        [6.0, 12.0, 20.0]
    ])
    b = np.array([B0, B1, B2])
    coeffs_345 = np.linalg.solve(A, b)
    
    return (float(c0), float(c1), float(c2), float(coeffs_345[0]), float(coeffs_345[1]), float(coeffs_345[2]))


_HERMITE_COEFFS = _compute_hermite_coeffs()


def xi_blend(r: ArrayLike, M: float, G_CONST: float = G, c_CONST: float = C) -> ArrayLike:
    """
    Blend zone Segment Density, valid for 1.8 <= r/r_s <= 2.2.
    Uses C² continuous Hermite interpolation.
    """
    r_arr = np.asarray(r, dtype=float)
    r_s = characteristic_radius(M, G_CONST, c_CONST)
    x = r_arr / r_s
    
    dx = X_BLEND_MAX - X_BLEND_MIN
    t = (x - X_BLEND_MIN) / dx
    
    a0, a1, a2, a3, a4, a5 = _HERMITE_COEFFS
    
    xi = a0 + a1*t + a2*t**2 + a3*t**3 + a4*t**4 + a5*t**5
    return float(xi) if r_arr.ndim == 0 else xi


def xi_canonical(r: ArrayLike, M: float, G_CONST: float = G, c_CONST: float = C) -> ArrayLike:
    """
    Canonical piecewise Segment Density Xi(r) across all branches.
    """
    r_arr = np.asarray(r, dtype=float)
    r_s = characteristic_radius(M, G_CONST, c_CONST)
    x = r_arr / r_s
    
    if r_arr.ndim == 0:
        if x < X_BLEND_MIN:
            return float(xi_strong(r, M, G_CONST, c_CONST))
        elif x <= X_BLEND_MAX:
            return float(xi_blend(r, M, G_CONST, c_CONST))
        else:
            return float(xi_weak(r, M, G_CONST, c_CONST))
            
    xi_res = np.zeros_like(r_arr)
    
    strong_mask = x < X_BLEND_MIN
    blend_mask = (x >= X_BLEND_MIN) & (x <= X_BLEND_MAX)
    weak_mask = x > X_BLEND_MAX
    
    if np.any(strong_mask):
        xi_res[strong_mask] = xi_strong(r_arr[strong_mask], M, G_CONST, c_CONST)
    if np.any(blend_mask):
        xi_res[blend_mask] = xi_blend(r_arr[blend_mask], M, G_CONST, c_CONST)
    if np.any(weak_mask):
        xi_res[weak_mask] = xi_weak(r_arr[weak_mask], M, G_CONST, c_CONST)
        
    return xi_res


# ============================================================================
# CANONICAL AXIOMATIC SCALING FUNCTIONS (Derived from Xi)
# ============================================================================

def D_from_xi(xi: ArrayLike) -> ArrayLike:
    """
    Time-dilation factor D(r) derived directly from primary Segment Density Xi:
    D = 1 / (1 + Xi)
    """
    return 1.0 / (1.0 + xi)


def s_from_xi(xi: ArrayLike) -> ArrayLike:
    """
    Radial-stretching factor s(r) derived directly from primary Segment Density Xi:
    s = 1 + Xi
    """
    return 1.0 + xi


def gamma_from_xi(xi: ArrayLike) -> ArrayLike:
    """
    Lorentz rapidity factor gamma(r) derived directly from primary Segment Density Xi:
    gamma = 1 + Xi
    """
    return 1.0 + xi


def beta_from_gamma(gamma: ArrayLike) -> ArrayLike:
    """
    Derived velocity field beta(r) calculated from rapidity:
    beta = sqrt(1 - 1/gamma²)
    """
    gam_arr = np.asarray(gamma, dtype=float)
    inside = np.maximum(1.0 - 1.0 / (gam_arr ** 2), 0.0)
    return np.sqrt(inside)


# ============================================================================
# REGIME ROUTING ENGINE
# ============================================================================

def regime_of_r(r: float, M: float) -> str:
    """
    Return the physical regime of a coordinate radius r.
    Regime table:
    r_s/r < 1.8       -> very_close
    1.8 - 2.2         -> blended
    2.2 - 3.0         -> photon_sphere
    3.0 - 10.0        -> strong
    > 10.0            -> weak
    """
    r_s = characteristic_radius(M)
    x = r / r_s
    
    if x < 1.8:
        return "very_close"
    elif x <= 2.2:
        return "blended"
    elif x <= 3.0:
        return "photon_sphere"
    elif x <= 10.0:
        return "strong"
    else:
        return "weak"
