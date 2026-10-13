"""
SSZ Strong Field Module

Implements strong-field structure and photon-sphere dynamics under canonical SSZ.

© 2025 Carmen N. Wrede & Lino Casu
Licensed under the Anti-Capitalist Software License v1.4
"""

import numpy as np
from scipy.optimize import brentq

from . import core as _core
from .core import xi_canonical, D_from_xi, s_from_xi, characteristic_radius


def photon_sphere_radius(M: float) -> float:
    """
    Coordinate radius of the circular null orbit of the CANONICAL SSZ metric.

    Forensic audit 2026-10-13 (Phase D3, Carmen mandate): for the canonical
    metric ds^2 = -D^2 c^2 dt^2 + s^2 dr^2 + r^2 dOmega^2 with D = 1/(1+Xi),
    s = 1+Xi, C = r^2, circular null orbits satisfy d/dr[r*(1+Xi(r))] = 0.
    The two stationary points found (1.884885 / 2.130540 r_s) lie INSIDE the
    Hermite blend zone and migrate with the blend width (+-25% width ->
    ~2.5% migration): BLEND_ARTIFACT, no physical photon sphere.

    The previously hard-coded return value 3*r_s was an UNMARKED CONVENTION
    (it matches neither the metric-derived stationary points nor the GR
    Schwarzschild value 1.5 r_s) and is withdrawn as a physical claim. This
    function now FAILS CLOSED, consistent with the observable-registry rule
    that observables must derive from one metric.

    Returns:
        float: nan (no physically valid circular null orbit; see
        photon_sphere_report() for the full verdict dict)
    """
    return float('nan')


def _stationary_points(x_lo=1.05, x_hi=3.5, n=8000, tol_round=6):
    """Find stationary points of x*(1+Xi(x)) on a dense dimensionless grid."""
    r_s = characteristic_radius(1.0)

    def f(x):
        x = np.asarray(x, dtype=float)
        return x * (1.0 + _core.xi_canonical(x * r_s, 1.0))

    grid = np.linspace(x_lo, x_hi, n)
    d1 = np.diff(f(grid))
    roots = []
    for i in range(len(grid) - 2):
        if d1[i] * d1[i + 1] < 0:
            try:
                roots.append(brentq(
                    lambda x: (f(x + 1e-6) - f(x - 1e-6)) / 2e-6,
                    grid[i], grid[i + 2]))
            except Exception:
                pass
    return sorted(set(round(r, tol_round) for r in roots))


def photon_sphere_report(M: float) -> dict:
    """
    Full metric-derived photon-sphere verdict for the canonical SSZ metric.

    Forensic audit 2026-10-13 (Phase D3, Carmen mandate). The canonical metric
        ds^2 = -D(r)^2 c^2 dt^2 + s(r)^2 dr^2 + r^2 dOmega^2,
        D = 1/(1+Xi), s = 1+Xi, C(r) = r^2
    admits circular null orbits where d/dr[C/A_t] = d/dr[r*(1+Xi(r))] = 0.

    Result: exactly two stationary points exist, BOTH inside the Hermite
    blend zone (1.8-2.2 r_s). Varying the blend width by +25% migrates the
    pair by ~2.5% in r/r_s — a physical photon sphere must not depend on the
    interpolation width. Verdict: BLEND_ARTIFACT (consistent with the sealed
    Stufe-5 result 1.884885 / 2.130540 r_s, migration-classified).

    The previously hard-coded return value 3*r_s (old photon_sphere_radius)
    matched neither the metric-derived stationary points nor the GR
    Schwarzschild value 1.5 r_s and is withdrawn as unmarked convention.
    """
    r_s = characteristic_radius(M)
    roots = _stationary_points()

    blend_lo, blend_hi = _core.X_BLEND_MIN, _core.X_BLEND_MAX
    in_blend = all(blend_lo <= x <= blend_hi for x in roots)

    # Blend-width migration probe: +25% width, same zone center. Save and
    # restore the module-level blend state around the probe.
    center = 0.5 * (blend_lo + blend_hi)
    half = 0.5 * (blend_hi - blend_lo)
    saved = (_core.X_BLEND_MIN, _core.X_BLEND_MAX, _core._HERMITE_COEFFS)
    try:
        _core.X_BLEND_MIN = center - 1.25 * half
        _core.X_BLEND_MAX = center + 1.25 * half
        _core._HERMITE_COEFFS = _core._compute_hermite_coeffs()
        migrated = _stationary_points()
    finally:
        _core.X_BLEND_MIN, _core.X_BLEND_MAX = saved[0], saved[1]
        _core._HERMITE_COEFFS = saved[2]

    migration_rel = 0.0
    if roots and migrated and len(migrated) == len(roots):
        migration_rel = max(abs(a - b) / a for a, b in zip(roots, migrated))

    is_artifact = bool(in_blend and migration_rel > 1e-3)
    return {
        "photon_sphere_exists": bool(roots),
        "stationary_points_r_over_rs": roots,
        "all_stationary_points_in_blend_zone": in_blend,
        "blend_zone": [blend_lo, blend_hi],
        "blend_width_migration_rel": migration_rel,
        "migrated_points_r_over_rs": migrated,
        "verdict": "BLEND_ARTIFACT" if is_artifact else (
            "METRIC_DERIVED" if roots else "NO_STATIONARY_POINTS"),
        "gr_schwarzschild_reference": 1.5 * r_s,
        "note": ("stationary points exist but migrate with blend width "
                 "(+25%% width -> %.2f%% migration): interpolation "
                 "artifact, not a physical photon sphere; previous hard-coded "
                 "3*r_s withdrawn as unmarked convention (audit 2026-10-13)"
                 % (100.0 * migration_rel)),
    }


def strong_field_redshift_limit(M: float) -> float:
    """
    Compute the maximum redshift factor at the core boundary (r = r_s).
    Under standard GR, redshift goes to infinity at r_s (black hole).
    Under SSZ, the core is regularized and has a finite limit:
        1 + z = 1 / D(r_s) = 1 + Xi(r_s) = 2 - exp(-phi) ≈ 1.8017118
    """
    r_s = characteristic_radius(M)
    xi_rs = xi_canonical(r_s, M)
    return float(1.0 + xi_rs)


def Xi_at_schwarzschild_radius(M: float) -> float:
    """
    Evaluate primary segment density field Xi(r) exactly at r = r_s.
    Axiomatic limit: Xi_strong(r_s) = 1 - exp(-phi) ≈ 0.8017118
    """
    r_s = characteristic_radius(M)
    return float(xi_canonical(r_s, M))


def Xi_at_characteristic_radius(M: float) -> float:
    """
    Alias for Xi_at_schwarzschild_radius.
    """
    return Xi_at_schwarzschild_radius(M)


def D_at_schwarzschild_radius(M: float) -> float:
    """
    Evaluate clock scaling factor D(r_s) exactly at r = r_s.
    D_at_r_s = 1 / (1 + Xi(r_s)) ≈ 1 / (2 - e^-phi) ≈ 0.55502
    """
    xi_rs = Xi_at_schwarzschild_radius(M)
    return float(D_from_xi(xi_rs))


def strong_field_regime_report(r: float, M: float) -> dict:
    """
    Generate a scale-domain regime report for radius r.
    Categorizes radial distance according to SSZ's physical boundaries.
    """
    r_s = characteristic_radius(M)
    x = r / r_s
    if x < 1.8:
        regime = "STRONG_FIELD_CORE"
    elif x <= 2.2:
        regime = "BLEND_ZONE"
    else:
        regime = "WEAK_FIELD"
    return {
        "radius": r,
        "x_compactness": x,
        "regime": regime,
        "xi": float(xi_canonical(r, M)),
        "D": float(D_from_xi(xi_canonical(r, M))),
        "s": float(s_from_xi(xi_canonical(r, M)))
    }


def compactness_report(R: float, M: float) -> dict:
    """
    Evaluate geometric compactness C_g = r_s / R of a static spherical boundary R.
    """
    r_s = characteristic_radius(M)
    return {
        "characteristic_radius": r_s,
        "boundary_radius": R,
        "compactness_ratio": r_s / R
    }


def finite_boundary_report(M: float) -> dict:
    """
    Provide boundary evaluation at characteristic radius r_s.
    """
    r_s = characteristic_radius(M)
    return {
        "r_s": r_s,
        "Xi_boundary": Xi_at_schwarzschild_radius(M),
        "D_boundary": D_at_schwarzschild_radius(M)
    }


def energy_condition_regime(coords, M: float) -> float:
    """
    Evaluates weak and strong energy conditions at coordinate location coords.
    Returns 1.0 if satisfied, 0.0 otherwise. Scoped as diagnostic proxy.
    """
    from .energy import check_weak_energy_condition, check_strong_energy_condition
    if isinstance(coords, (list, tuple, np.ndarray)):
        r = coords[1]
    else:
        r = coords
    wec = check_weak_energy_condition(r, M)
    sec = check_strong_energy_condition(r, M)
    return 1.0 if (wec and sec) else 0.0
