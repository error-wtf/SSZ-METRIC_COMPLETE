"""
SSZ Parameterized Post-Newtonian (PPN) Module

PPN parameters are DERIVED from the actual weak-field metric branch
    A_t(r) = (1 + u)^-2,  B_r(r) = (1 + u)^2,  u = r_s/(2r)
by transforming to isotropic coordinates and reading the 1/rho and
1/rho^2 coefficients of g_tt and g_rr. No parameter is hard-coded.

Verified results (forensic audit 2026-10-13, symbolic + numeric):
    beta_PPN = 5/2   (metric property: -g_tt/c^2 = 1 - 2U + 5U^2 in isotropic coords)
    gamma_PPN = 1    (to first order)
The previous version returned hard-coded 1.0/1.0, which did NOT follow from
the implemented metric. Independent symbolic proof:
    GLOBAL_FORENSIC_V1/symbolic_reference_case.py (GR control (1, 1/4) recovered).

[REPAIR 2026-10-13, forensic audit Phase C: PPN values now computed from the
metric via numeric isotropic-coordinate fit; GR self-check included.]

© 2025 Carmen N. Wrede & Lino Casu
Licensed under the Anti-Capitalist Software License v1.4
"""

import numpy as np
from scipy.interpolate import CubicSpline
from .constants import C
from .core import characteristic_radius


def _isotropic_ppn_fit(A_t, B_r, r_s, r_min_mult=3.0, r_max_mult=20000.0, n=300000,
                       fit_rmin_mult=50.0, deg=4):
    """
    General PPN extraction for a static diagonal metric ds^2 = -A_t c^2 dt^2 + B_r dr^2.

    Conformally flat (isotropic) radius (GENERAL construction, not the naive
    d rho/dr = 1/sqrt(B_r) which is only valid for special metrics):
        d rho/rho = sqrt(B_r) dr/r  ->  rho(r) = r * K(r),
        K(r) = exp( - int_r^rmax (sqrt(B_r(s)) - 1)/s ds )   [convergent; rho/r -> 1]

    Analytic checks (sympy, exact):
        SSZ weak: rho = r*exp(-1/(2r)) (Lambert-W invertible);
            -g_tt/c^2 = 1 - 1/rho + 5/(4 rho^2) - 13/(8 rho^3) => beta = 5/2,
            g_rr^iso  = 1 + 1/rho + 1/(24 rho^3)               => gamma = 1.
        GR (Schwarzschild): beta = gamma = 1.
    [NOTE: an earlier draft of this repair used the naive d rho/dr = 1/sqrt(B_r);
     that ODE is only valid for special metrics and gave GR gamma = 2.0 — wrong.
     The conformally-flat construction above is metric-general.]

    Fits on a UNIFORM 1/rho grid in [1/rmax, 1/(50 r_s)], polynomial degree 4
    (absorbs 1/rho^3 and 1/rho^4 truncation terms; a1, a2, b1 read from the
    degree-4 coefficients). Validation (r_s = 1):
        SSZ: rs_meas = 1.0000249, beta = 2.4999641, gamma = 0.99995005
        GR : rs_meas = 1.0000250, beta = 0.9999997, gamma = 0.9999500
    """
    r = np.logspace(np.log10(r_s * r_min_mult), np.log10(r_s * r_max_mult), n)
    sBr = np.sqrt(B_r(r))
    integrand = (sBr - 1.0) / r
    # I(r) = int_r^rmax integrand ds (trapezoid, from the top down)
    I = np.zeros_like(r)
    avg = 0.5 * (integrand[:-1] + integrand[1:])          # length n-1
    dr = np.diff(r)                                        # length n-1
    I[:-1] = np.cumsum((avg * dr)[::-1])[::-1]
    K = np.exp(-I)
    rho = r * K
    order = np.argsort(rho)
    inv = CubicSpline(rho[order], r[order])          # r(rho)

    # Fit window: uniform in x = 1/rho, rho in [50 r_s, r_max]
    x = np.linspace(1.0 / (r_s * r_max_mult), 1.0 / (r_s * fit_rmin_mult), 8000)
    rho_u = 1.0 / x
    r_of_rho = inv(rho_u)

    y_tt = A_t(r_of_rho)               # -g_tt/c^2
    y_rr = (r_of_rho / rho_u)**2       # g_rr in isotropic coords = (r/rho)^2 (exact by construction)

    c_tt = np.polyfit(x, y_tt, deg)
    c_rr = np.polyfit(x, y_rr, deg)
    a2, a1 = c_tt[-3], c_tt[-2]
    b1 = c_rr[-2]
    a0 = c_tt[-1]
    b0 = c_rr[-1]

    rs_meas = -a1                      # r_s implied by g_tt
    beta = 2.0 * a2 / rs_meas**2
    gamma = b1 / (-a1)
    return {
        "a0": a0, "b0": b0,
        "rs_meas_over_rs_input": float(rs_meas / r_s),
        "beta_ppn": float(beta),
        "gamma_ppn": float(gamma),
        "fit_residual_gtt": float(np.max(np.abs(np.polyval(c_tt, x) - y_tt))),
        "fit_residual_grr": float(np.max(np.abs(np.polyval(c_rr, x) - y_rr))),
    }


def _weak_branch_metric(r):
    u = 1.0 / (2.0 * r)  # units of r_s = 1
    return (1.0 + u)**-2, (1.0 + u)**2


def ppn_parameters_from_metric() -> dict:
    """
    Derive PPN parameters of the weak-field SSZ branch from the metric itself.
    Includes the Schwarzschild GR control in the SAME numeric pipeline.
    """
    ssz = _isotropic_ppn_fit(lambda r: _weak_branch_metric(r)[0],
                             lambda r: _weak_branch_metric(r)[1], r_s=1.0)

    gr = _isotropic_ppn_fit(lambda r: 1.0 - 1.0/r, lambda r: 1.0/(1.0 - 1.0/r), r_s=1.0)
    return {"ssz_weak_branch": ssz, "gr_control": gr}


_CACHE = None


def beta_ppn_parameter() -> float:
    """
    PPN beta of the weak-field SSZ branch, DERIVED from the metric.
    Metric property: -g_tt/c^2 = 1 - 2U + 5U^2 (isotropic) => beta = 5/2.
    """
    global _CACHE
    if _CACHE is None:
        _CACHE = ppn_parameters_from_metric()
    return _CACHE["ssz_weak_branch"]["beta_ppn"]


def gamma_ppn_parameter() -> float:
    """
    PPN gamma of the weak-field SSZ branch, DERIVED from the metric.
    """
    global _CACHE
    if _CACHE is None:
        _CACHE = ppn_parameters_from_metric()
    return _CACHE["ssz_weak_branch"]["gamma_ppn"]


def ppn_gamma() -> float:
    """Alias for gamma_ppn_parameter."""
    return gamma_ppn_parameter()


def ppn_beta() -> float:
    """Alias for beta_ppn_parameter."""
    return beta_ppn_parameter()


def lensing_deflection_ppn(r_s: float, b: float, gamma_ppn: float = None) -> float:
    """
    First-order light deflection angle under PPN completion.
    alpha = (1 + gamma_ppn) * r_s / b. gamma_ppn defaults to the derived value.
    """
    if gamma_ppn is None:
        gamma_ppn = gamma_ppn_parameter()
    return float((1.0 + gamma_ppn) * r_s / b)


def shapiro_delay_ppn(r_s: float, r1: float, r2: float, d: float, gamma_ppn: float = None) -> float:
    """
    Shapiro time delay under PPN completion (one-way, radial, far-field):
    delta_t = (1 + gamma_ppn) * GM/c^3 * ln(4 r1 r2 / d^2)
            = (1 + gamma_ppn) * (r_s / 2C) * ln(4 r1 r2 / d^2).
    gamma_ppn defaults to the derived value.
    [REPAIR 2026-10-13: previous version used (r_s/C) — factor 2 too large
    (confused r_s=2GM/c^2 with GM/c^2). GR value (gamma=1) now = 2GM/c^3 ln(...) ✓]
    """
    if gamma_ppn is None:
        gamma_ppn = gamma_ppn_parameter()
    val = (4.0 * r1 * r2) / (d ** 2)
    return float((1.0 + gamma_ppn) * (r_s / (2.0 * C)) * np.log(val))


def perihelion_precession_ppn(M: float, a: float, e: float) -> float:
    """
    PPN perihelion precession per orbit INCLUDING the beta-dependent term:
    delta_omega = 3*pi*r_s/(a(1-e^2)) * [(2 + 2*gamma - beta)/3] / ... ;
    the standard GR value 6*pi*GM/(a(1-e^2)c^2) corresponds to beta=gamma=1.
    With the derived beta=5/2 this is NOT the GR value any more; we return the
    general 2PN-consistent expression used in PPN literature:
    delta_omega = (6*pi*GM/(a(1-e^2)c^2)) * (2 + 2*gamma - beta)/3.
    [REPAIR 2026-10-13: previous version silently used the pure-GR formula.]
    """
    r_s = characteristic_radius(M)
    base = 3.0 * np.pi * r_s / (a * (1.0 - e**2))
    factor = (2.0 + 2.0 * gamma_ppn_parameter() - beta_ppn_parameter()) / 3.0
    return float(base * factor)


def weak_field_expansion_coeffs(r: float, M: float) -> dict:
    """
    Areal-coordinate weak-field expansion of the ACTUAL metric branch
    A_t = (1+u)^-2, B_r = (1+u)^2, u = r_s/(2r) = U:
        -g_tt/c^2 = (1+U)^-2 = 1 - 2U + 3U^2 - 4U^3 + ...
        +g_rr     = (1+U)^2  = 1 + 2U + 1U^2
    [REPAIR 2026-10-13: previous version claimed 2U^2 (g_tt) and 3U^2 (g_rr),
    which matches neither the areal metric nor its isotropic form (5U^2).]
    """
    r_s = characteristic_radius(M)
    U = r_s / (2.0 * r)

    return {
        "U": U,
        "coordinates": "areal",
        "g_tt_coeff_order1": -2.0,
        "g_tt_coeff_order2": 3.0,
        "g_rr_coeff_order1": 2.0,
        "g_rr_coeff_order2": 1.0,
        "note_isotropic": "-g_tt/c^2 = 1 - 2U + 5U^2 in isotropic coordinates (beta=5/2)",
    }


__all__ = [
    'ppn_parameters_from_metric',
    'beta_ppn_parameter',
    'gamma_ppn_parameter',
    'ppn_gamma',
    'ppn_beta',
    'lensing_deflection_ppn',
    'shapiro_delay_ppn',
    'perihelion_precession_ppn',
    'weak_field_expansion_coeffs',
]
