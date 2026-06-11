"""
SSZ Canonical Pure Metric Module

This module implements the canonical SSZ metric tensor, its inverse, and determinant
directly from the primary Segment Density field Xi(r), ensuring that the
segmentation itself is the fundamental generating principle of the spacetime metric.

Axiomatic SSZ Metric:
    ds² = -c² * D(Xi(r))² dT² + s(Xi(r))² dr² + r²dΩ²
    where:
        D(Xi) = 1 / (1 + Xi(r))
        s(Xi) = 1 + Xi(r)

No GR, standard static diagonal, or rotating scaffolds are imported
or used inside this module.

© 2025 Carmen N. Wrede & Lino Casu
Licensed under the Anti-Capitalist Software License v1.4
"""

import numpy as np
from typing import Tuple, Union

from .constants import G, C, PHI, M_SUN
from .core import (
    xi_canonical, D_from_xi, s_from_xi, gamma_from_xi, beta_from_gamma, regime_of_r
)

# ============================================================================
# CANONICAL DIAGONS & TENSORS FROM PRIMARY SEGMENT DENSITY FIELD
# ============================================================================

def metric_diagonal(coords: Union[Tuple, np.ndarray], M: float, G_CONST: float = G, c_CONST: float = C) -> np.ndarray:
    """
    Compute the canonical diagonal 4x4 SSZ-Core metric tensor.
    Coords: (T, r, theta, phi)
    
    Axiomatic SSZ Formula:
        ds² = -D(Xi(r))² * c² dT² + s(Xi(r))² dr² + r²dθ² + r²sin²θ dφ²
        where:
            D(Xi) = 1 / (1 + Xi(r))
            s(Xi) = 1 + Xi(r)
    """
    T, r, theta, phi = coords
    
    # Evaluate primary physical Segment Density field first
    xi = xi_canonical(r, M, G_CONST, c_CONST)
    
    # Derive physical dilation and radial stretching directly from the primary field
    D = D_from_xi(xi)
    s = s_from_xi(xi)
    
    g = np.zeros((4, 4))
    g[0, 0] = -(D ** 2) * (c_CONST ** 2)
    g[1, 1] = s ** 2
    g[2, 2] = r * r
    g[3, 3] = r * r * (np.sin(theta) ** 2)
    
    return g


def inverse_metric_diagonal(coords: Union[Tuple, np.ndarray], M: float, G_CONST: float = G, c_CONST: float = C) -> np.ndarray:
    """
    Compute the exact 4x4 inverse of the diagonal SSZ-Core metric tensor.
    Derived axiomatically from primary Segment Density field.
    """
    T, r, theta, phi = coords
    
    xi = xi_canonical(r, M, G_CONST, c_CONST)
    D = D_from_xi(xi)
    s = s_from_xi(xi)
    
    g_inv = np.zeros((4, 4))
    g_inv[0, 0] = -1.0 / ((D ** 2) * (c_CONST ** 2))
    g_inv[1, 1] = 1.0 / (s ** 2)
    g_inv[2, 2] = 1.0 / (r * r)
    
    sin_th = np.sin(theta)
    g_inv[3, 3] = 1.0 / ((r * r) * (sin_th * sin_th)) if abs(sin_th) > 1e-15 else 0.0
    
    return g_inv


def det_metric_diagonal(coords: Union[Tuple, np.ndarray], M: float, G_CONST: float = G, c_CONST: float = C) -> float:
    """
    Compute the determinant of the diagonal SSZ-Core metric tensor.
    
    Identity:
        det(g) = g_TT * g_rr * g_thth * g_phph
               = (-D(Xi)² * c²) * (s(Xi)²) * r² * (r²sin²θ)
               = -c² * D(Xi)² * s(Xi)² * r⁴ sin²θ
               = -c² * (D*s)² * r⁴ sin²θ
               = -c² r⁴ sin²θ     (since D*s == 1 identically!)
    """
    T, r, theta, phi = coords
    sin_th = np.sin(theta)
    return -(c_CONST ** 2) * (r ** 4) * (sin_th * sin_th)


def metric_components(coords: Union[Tuple, np.ndarray], M: float, G_CONST: float = G, c_CONST: float = C) -> dict:
    """
    Compute metric components and diagnostic parameters.
    """
    T, r, theta, phi = coords
    xi = xi_canonical(r, M, G_CONST, c_CONST)
    D = D_from_xi(xi)
    s = s_from_xi(xi)
    gamma = gamma_from_xi(xi)
    regime = regime_of_r(r, M)
    det_g = det_metric_diagonal(coords, M, G_CONST, c_CONST)
    
    return {
        "xi": float(xi),
        "D": float(D),
        "s": float(s),
        "gamma": float(gamma),
        "regime": regime,
        "determinant": float(det_g)
    }


def metric_flow_form(coords: Union[Tuple, np.ndarray], M: float, G_CONST: float = G, c_CONST: float = C) -> np.ndarray:
    """
    Compute the canonical non-diagonal flow (river/spiral) form of the SSZ-Core metric.
    Coords: (t, r, theta, phi)
    
    Axiomatic SSZ Formula:
        ds² = -c²(1 - β(Xi)²) dt² + 2β(Xi)c dt dr + dr² + r²dΩ²
    """
    t, r, theta, phi = coords
    
    xi = xi_canonical(r, M, G_CONST, c_CONST)
    gamma = gamma_from_xi(xi)
    beta = beta_from_gamma(gamma)
    
    g = np.zeros((4, 4))
    g[0, 0] = -(c_CONST ** 2) * (1.0 - beta * beta)
    g[1, 1] = 1.0
    g[2, 2] = r * r
    g[3, 3] = r * r * (np.sin(theta) ** 2)
    
    g_tr = beta * c_CONST
    g[0, 1] = g_tr
    g[1, 0] = g_tr
    
    return g
