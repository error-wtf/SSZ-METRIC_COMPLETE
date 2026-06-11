"""
SSZ Curvature Tensor and Connection Engine

This module provides symbolic and numerical calculations of:
- Metric Derivatives
- Christoffel Symbols (connection) Γ^μ_νρ
- Riemann Curvature Tensor R^λ_μνρ
- Ricci Curvature Tensor R_μν
- Ricci Curvature Scalar R
- Einstein Curvature Tensor G_μν

The numerical engine operates on any coordinate-dependent 4D metric function g_func(x)
by performing exact finite differences around the 4-vector coordinate x.

© 2025 Carmen Wrede & Lino Casu
Licensed under the Anti-Capitalist Software License v1.4
"""

import numpy as np
import warnings
from typing import Tuple, Callable, Dict, Any, Union

try:
    import sympy as sp
    SYMPY_AVAILABLE = True
except ImportError:
    SYMPY_AVAILABLE = False


# ============================================================================
# NUMERICAL TENSOR GEOMETRY ENGINE
# ============================================================================

def numerical_derivative_metric(
    g_func: Callable[[Union[Tuple, np.ndarray]], np.ndarray],
    x: Union[Tuple, np.ndarray],
    h: float = 1e-5
) -> np.ndarray:
    """
    Compute the first partial derivative of the metric: ∂_α g_βγ.
    Evaluated at coordinate 4-vector x = (x⁰, x¹, x², x³).
    
    Returns:
        dg[alpha, beta, gamma]: 4x4x4 array of derivatives
    """
    x_arr = np.array(x, dtype=float)
    dg = np.zeros((4, 4, 4))
    
    for alpha in range(4):
        x_plus = x_arr.copy()
        x_minus = x_arr.copy()
        
        x_plus[alpha] += h
        x_minus[alpha] -= h
        
        g_plus = g_func(x_plus)
        g_minus = g_func(x_minus)
        
        dg[alpha] = (g_plus - g_minus) / (2.0 * h)
        
    return dg


def christoffel_symbols(
    g_func: Callable[[Union[Tuple, np.ndarray]], np.ndarray],
    x: Union[Tuple, np.ndarray],
    h: float = 1e-5
) -> np.ndarray:
    """
    Compute Christoffel symbols Γ^μ_νρ at coordinate x.
    Γ^μ_νρ = 0.5 * g^μσ * (∂_ν g_σρ + ∂_ρ g_νσ - ∂_σ g_νρ)
    """
    g = g_func(x)
    g_inv = np.linalg.inv(g)
    
    # Compute ∂_α g_βγ
    dg = numerical_derivative_metric(g_func, x, h)
    
    Gamma = np.zeros((4, 4, 4))
    
    for mu in range(4):
        for nu in range(4):
            for rho in range(4):
                val = 0.0
                for sig in range(4):
                    val += 0.5 * g_inv[mu, sig] * (
                        dg[nu, sig, rho] + dg[rho, nu, sig] - dg[sig, nu, rho]
                    )
                Gamma[mu, nu, rho] = val
                
    return Gamma


def riemann_tensor(
    g_func: Callable[[Union[Tuple, np.ndarray]], np.ndarray],
    x: Union[Tuple, np.ndarray],
    h: float = 1e-5
) -> np.ndarray:
    """
    Compute Riemann curvature tensor R^λ_μνρ at coordinate x.
    R^λ_μνρ = ∂_ν Γ^λ_μρ - ∂_ρ Γ^λ_μν + Γ^λ_σν Γ^σ_μρ - Γ^λ_σρ Γ^σ_μν
    """
    x_arr = np.array(x, dtype=float)
    
    # Compute derivatives of Christoffels: dGamma[alpha, lambda, mu, nu] = ∂_alpha Γ^lambda_mu_nu
    dGamma = np.zeros((4, 4, 4, 4))
    
    for alpha in range(4):
        x_plus = x_arr.copy()
        x_minus = x_arr.copy()
        
        x_plus[alpha] += h
        x_minus[alpha] -= h
        
        Gamma_plus = christoffel_symbols(g_func, x_plus, h)
        Gamma_minus = christoffel_symbols(g_func, x_minus, h)
        
        dGamma[alpha] = (Gamma_plus - Gamma_minus) / (2.0 * h)
        
    Gamma = christoffel_symbols(g_func, x, h)
    
    R = np.zeros((4, 4, 4, 4))
    for lam in range(4):
        for mu in range(4):
            for nu in range(4):
                for rho in range(4):
                    term1 = dGamma[nu, lam, mu, rho]
                    term2 = dGamma[rho, lam, mu, nu]
                    term3 = sum(Gamma[lam, sig, nu] * Gamma[sig, mu, rho] for sig in range(4))
                    term4 = sum(Gamma[lam, sig, rho] * Gamma[sig, mu, nu] for sig in range(4))
                    
                    R[lam, mu, nu, rho] = term1 - term2 + term3 - term4
                    
    return R


def ricci_tensor(
    g_func: Callable[[Union[Tuple, np.ndarray]], np.ndarray],
    x: Union[Tuple, np.ndarray],
    h: float = 1e-5
) -> np.ndarray:
    """
    Compute Ricci curvature tensor R_μν at coordinate x.
    R_μν = R^λ_μλν
    """
    R_riemann = riemann_tensor(g_func, x, h)
    R_ricci = np.zeros((4, 4))
    for mu in range(4):
        for nu in range(4):
            R_ricci[mu, nu] = sum(R_riemann[lam, mu, lam, nu] for lam in range(4))
    return R_ricci


def ricci_scalar(
    g_func: Callable[[Union[Tuple, np.ndarray]], np.ndarray],
    x: Union[Tuple, np.ndarray],
    h: float = 1e-5
) -> float:
    """
    Compute Ricci curvature scalar R at coordinate x.
    R = g^μν R_μν
    """
    g = g_func(x)
    g_inv = np.linalg.inv(g)
    R_ricci = ricci_tensor(g_func, x, h)
    return float(np.sum(g_inv * R_ricci))


def einstein_tensor(
    g_func: Callable[[Union[Tuple, np.ndarray]], np.ndarray],
    x: Union[Tuple, np.ndarray],
    h: float = 1e-5
) -> np.ndarray:
    """
    Compute Einstein curvature tensor G_μν at coordinate x.
    G_μν = R_μν - 0.5 * R * g_μν
    """
    g = g_func(x)
    R_ricci = ricci_tensor(g_func, x, h)
    R_scalar = ricci_scalar(g_func, x, h)
    return R_ricci - 0.5 * R_scalar * g


# ============================================================================
# ANALYTICAL TENSOR GEOMETRY ENGINE (SYMPY)
# ============================================================================

def symbolic_curvature_diagonal(
    g_tt: Any,
    g_rr: Any,
    g_thth: Any,
    g_phph: Any,
    coords_symbols: Tuple[Any, Any, Any, Any]
) -> Dict[str, Any]:
    """
    Perform exact analytical symbolic curvature derivation for a general diagonal metric.
    """
    if not SYMPY_AVAILABLE:
        raise RuntimeError("SymPy is not installed - symbolic computation is unavailable.")
        
    x = coords_symbols
    g = sp.Matrix([
        [g_tt, 0, 0, 0],
        [0, g_rr, 0, 0],
        [0, 0, g_thth, 0],
        [0, 0, 0, g_phph]
    ])
    g_inv = g.inv()
    
    # Christoffel Γ^mu_nu_rho
    Gamma = [[[sp.Expr(0) for _ in range(4)] for _ in range(4)] for _ in range(4)]
    for mu in range(4):
        for nu in range(4):
            for rho in range(4):
                val = 0
                for sig in range(4):
                    dg_nu = sp.diff(g[sig, rho], x[nu])
                    dg_rho = sp.diff(g[nu, sig], x[rho])
                    dg_sig = sp.diff(g[nu, rho], x[sig])
                    val += 0.5 * g_inv[mu, sig] * (dg_nu + dg_rho - dg_sig)
                Gamma[mu][nu][rho] = sp.simplify(val)
                
    # Ricci R_mu_nu
    R_ricci = sp.Matrix.zeros(4, 4)
    for mu in range(4):
        for nu in range(4):
            val = 0
            for lam in range(4):
                term1 = sp.diff(Gamma[lam][mu][nu], x[lam])
                term2 = sp.diff(Gamma[lam][mu][lam], x[nu])
                term3 = sum(Gamma[lam][sig][lam] * Gamma[sig][mu][nu] for sig in range(4))
                term4 = sum(Gamma[lam][sig][nu] * Gamma[sig][mu][lam] for sig in range(4))
                val += term1 - term2 + term3 - term4
            R_ricci[mu, nu] = sp.simplify(val)
            
    # Ricci Scalar
    R_scalar = sp.simplify(sum(g_inv[i, j] * R_ricci[i, j] for i in range(4) for j in range(4)))
    
    # Einstein G_mu_nu
    G_einstein = sp.Matrix.zeros(4, 4)
    for mu in range(4):
        for nu in range(4):
            G_einstein[mu, nu] = sp.simplify(R_ricci[mu, nu] - 0.5 * R_scalar * g[mu, nu])
            
    return {
        "metric": g,
        "christoffel": Gamma,
        "ricci_tensor": R_ricci,
        "ricci_scalar": R_scalar,
        "einstein_tensor": G_einstein
    }
