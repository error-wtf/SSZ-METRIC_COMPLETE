"""
SSZ Spacetime Curvature Module

Implements numerical (finite-difference) and symbolic (SymPy) methods for:
- Christoffel symbols Γ^μ_νρ
- Riemann curvature tensor R^λ_μνρ
- Ricci curvature tensor R_μν
- Ricci scalar R
- Einstein tensor G_μν

Suitable for both spherically symmetric static and rotating Kerr-SSZ metrics.

© 2025 Carmen N. Wrede & Lino Casu
Licensed under the Anti-Capitalist Software License v1.4
"""

import numpy as np
import warnings
from typing import Tuple, Callable, Dict, Any

try:
    import sympy as sp
    SYMPY_AVAILABLE = True
except ImportError:
    SYMPY_AVAILABLE = False


# ============================================================================
# NUMERICAL GEOMETRY ENGINE (Finite Difference Method)
# ============================================================================

def christoffel_numerical(
    metric_func: Callable[[float, float, float, float], np.ndarray],
    coords: Tuple[float, float, float, float],
    eps: float = 1e-5
) -> np.ndarray:
    """
    Compute Christoffel symbols Γ^μ_νρ numerically.
    Γ^μ_νρ = 0.5 * g^μσ * (∂_ν g_σρ + ∂_ρ g_νσ - ∂_σ g_νρ)
    
    Args:
        metric_func: Function (t, r, theta, phi) -> 4x4 metric tensor
        coords: (t, r, theta, phi) coordinate values
        eps: Finite difference step size
    """
    t, r, theta, phi = coords
    g = metric_func(t, r, theta, phi)
    g_inv = np.linalg.inv(g)
    
    Gamma = np.zeros((4, 4, 4))
    coord_vals = [t, r, theta, phi]
    
    # Pre-calculate metric derivatives ∂_α g_βγ using central differences
    dg = np.zeros((4, 4, 4))  # dg[alpha, beta, gamma] = ∂_alpha g_beta_gamma
    for alpha in range(4):
        coords_plus = list(coord_vals)
        coords_minus = list(coord_vals)
        coords_plus[alpha] += eps
        coords_minus[alpha] -= eps
        
        g_plus = metric_func(*coords_plus)
        g_minus = metric_func(*coords_minus)
        
        dg[alpha] = (g_plus - g_minus) / (2 * eps)
        
    # Construct Γ^mu_nu_rho
    for mu in range(4):
        for nu in range(4):
            for rho in range(4):
                val = 0.0
                for sigma in range(4):
                    val += 0.5 * g_inv[mu, sigma] * (dg[nu, sigma, rho] + dg[rho, nu, sigma] - dg[sigma, nu, rho])
                Gamma[mu, nu, rho] = val
                
    return Gamma


def riemann_numerical(
    metric_func: Callable[[float, float, float, float], np.ndarray],
    coords: Tuple[float, float, float, float],
    eps: float = 1e-5
) -> np.ndarray:
    """
    Compute Riemann curvature tensor R^λ_μνρ numerically.
    R^λ_μνρ = ∂_ν Γ^λ_μρ - ∂_ρ Γ^λ_μν + Γ^λ_σν Γ^σ_μρ - Γ^λ_σρ Γ^σ_μν
    """
    t, r, theta, phi = coords
    R = np.zeros((4, 4, 4, 4))
    coord_vals = [t, r, theta, phi]
    
    # Precompute Christoffels at plus/minus epsilon for numerical derivative of Gamma
    dGamma = np.zeros((4, 4, 4, 4))  # dGamma[alpha, lambda, mu, nu] = ∂_alpha Γ^lambda_mu_nu
    for alpha in range(4):
        coords_plus = list(coord_vals)
        coords_minus = list(coord_vals)
        coords_plus[alpha] += eps
        coords_minus[alpha] -= eps
        
        Gamma_plus = christoffel_numerical(metric_func, tuple(coords_plus), eps)
        Gamma_minus = christoffel_numerical(metric_func, tuple(coords_minus), eps)
        
        dGamma[alpha] = (Gamma_plus - Gamma_minus) / (2 * eps)
        
    Gamma = christoffel_numerical(metric_func, coords, eps)
    
    for lam in range(4):
        for mu in range(4):
            for nu in range(4):
                for rho in range(4):
                    term1 = dGamma[nu, lam, mu, rho]
                    term2 = dGamma[rho, lam, mu, nu]
                    term3 = sum(Gamma[lam, sigma, nu] * Gamma[sigma, mu, rho] for sigma in range(4))
                    term4 = sum(Gamma[lam, sigma, rho] * Gamma[sigma, mu, nu] for sigma in range(4))
                    
                    R[lam, mu, nu, rho] = term1 - term2 + term3 - term4
                    
    return R


def ricci_numerical(
    metric_func: Callable[[float, float, float, float], np.ndarray],
    coords: Tuple[float, float, float, float],
    eps: float = 1e-5
) -> np.ndarray:
    """
    Compute Ricci curvature tensor R_μν numerically by contracting Riemann.
    R_μν = R^λ_μλν
    """
    R_riemann = riemann_numerical(metric_func, coords, eps)
    R_ricci = np.zeros((4, 4))
    for mu in range(4):
        for nu in range(4):
            R_ricci[mu, nu] = sum(R_riemann[lam, mu, lam, nu] for lam in range(4))
    return R_ricci


def einstein_numerical(
    metric_func: Callable[[float, float, float, float], np.ndarray],
    coords: Tuple[float, float, float, float],
    eps: float = 1e-5
) -> Tuple[np.ndarray, float, np.ndarray]:
    """
    Compute Einstein tensor G_μν, Ricci scalar R, and Ricci tensor.
    G_μν = R_μν - 0.5 * R * g_μν
    """
    t, r, theta, phi = coords
    g = metric_func(t, r, theta, phi)
    g_inv = np.linalg.inv(g)
    
    R_ricci = ricci_numerical(metric_func, coords, eps)
    
    # Ricci Scalar
    R_scalar = float(np.sum(g_inv * R_ricci))
    
    G_einstein = R_ricci - 0.5 * R_scalar * g
    
    return G_einstein, R_scalar, R_ricci


# ============================================================================
# SYMBOLIC GEOMETRY ENGINE (SymPy Analytical Solution)
# ============================================================================

def symbolic_curvature_diagonal(
    g_tt: sp.Expr,
    g_rr: sp.Expr,
    g_thth: sp.Expr,
    g_phph: sp.Expr,
    coords_symbols: Tuple[sp.Symbol, sp.Symbol, sp.Symbol, sp.Symbol]
) -> Dict[str, Any]:
    """
    Perform exact analytical symbolic curvature derivation for a general diagonal metric.
    
    Args:
        g_tt, g_rr, g_thth, g_phph: SymPy analytical expressions for the metric components.
        coords_symbols: SymPy Symbols representing coordinate system e.g. (t, r, theta, phi)
        
    Returns:
        Dict of SymPy matrices containing Christoffel, Riemann, Ricci, and Einstein tensors.
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
                for sigma in range(4):
                    dg_nu = sp.diff(g[sigma, rho], x[nu])
                    dg_rho = sp.diff(g[nu, sigma], x[rho])
                    dg_sigma = sp.diff(g[nu, rho], x[sigma])
                    val += 0.5 * g_inv[mu, sigma] * (dg_nu + dg_rho - dg_sigma)
                Gamma[mu][nu][rho] = sp.simplify(val)
                
    # Ricci R_mu_nu = ∂_lambda Γ^lambda_mu_nu - ∂_nu Γ^lambda_mu_lambda + Γ^lambda_sigma_lambda Γ^sigma_mu_nu - Γ^lambda_sigma_nu Γ^sigma_mu_lambda
    R_ricci = sp.Matrix.zeros(4, 4)
    for mu in range(4):
        for nu in range(4):
            val = 0
            for lam in range(4):
                term1 = sp.diff(Gamma[lam][mu][nu], x[lam])
                term2 = sp.diff(Gamma[lam][mu][lam], x[nu])
                term3 = sum(Gamma[lam][sigma][lam] * Gamma[sigma][mu][nu] for sigma in range(4))
                term4 = sum(Gamma[lam][sigma][nu] * Gamma[sigma][mu][lam] for sigma in range(4))
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
