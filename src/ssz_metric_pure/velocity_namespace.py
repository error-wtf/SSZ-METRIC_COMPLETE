"""
SSZ Velocity Namespace Module (E1)

Canonical separation of the six distinct velocity quantities that the SSZ
corpus (25 original papers) labels "v_fall", "v_escape", or "v_total" in
different places. ONE unique symbol per quantity, with definition, reference
frame, units, and validity domain.

The dual velocity product relation
    v_esc_dual * v_fall_dual = c^2
is an IDENTITY under the parametrization gamma := 1 + Xi with the GR redshift
mapping gamma_GR = 1/sqrt(1 - v^2/c^2) (Dual Velocities paper). It is NOT an
independent field equation (Lino's Audit C1, confirmed against primary texts).

Source map (pdftotext line refs, extraction 2026-10-13):
  V_DUAL    : DualVelocities Z.106ff  "By mapping gamma_s to the GR redshift
              factor we obtain v_fall/c = sqrt(r/r_s)"  (r > r_s ONLY)
  V_ESC_DUAL: same paper, v_esc = c*sqrt(r_s/r), dual partner
  V_LOCAL   : code kinematics.v_fall = c*beta(r); energy-budget velocity,
              closest corpus analogue to the segment-structure rate
  V_BUCH    : SSZ_BOOK_EN_FINAL_BEST_VERSION.md Z.9368  c/sqrt(1+Xi)=0.866c
              (book worked example; NOT implemented in code, NOT dual)
  V_SEGMENT : OntheMetricofBlackHoles Z.209/Z.212 — qualitative only, no
              formula in the whole corpus (Lino-Audit C3: transport law OPEN)
  V_NEWTON  : AdditiveDecomposition Z.76  v_fall := sqrt(2GM/r) — escape-
              expression under a different name, radially inverted usage

© 2026 Carmen N. Wrede, Lino P. Casu & Bingsi
Licensed under the Anti-Capitalist Software License v1.4
"""

import numpy as np
from typing import Union

from .constants import C, G
from .core import characteristic_radius, xi_canonical

ArrayLike = Union[float, np.ndarray]

__all__ = [
    "V_DUAL", "V_ESC_DUAL", "V_LOCAL", "V_BUCH", "V_SEGMENT_LIMIT", "V_NEWTON",
    "v_dual", "v_esc_dual", "v_local", "v_buch", "v_newton",
    "dual_product_identity_residual", "identity_test_report",
    "VELOCITY_NAMESPACE_DOC",
]


# ============================================================================
# E1: THE SIX QUANTITIES — unique symbols, definitions, frames, domains
# ============================================================================

VELOCITY_NAMESPACE_DOC = {
    "v_dual": (
        "V_DUAL (dual fall velocity, coordinate)",
        "v_dual = c*sqrt(r/r_s)",
        "coordinate speed w.r.t. areal radius r; NOT a local particle speed "
        "(superluminal for r > r_s by construction)",
        "r > r_s ONLY (paper: 'for r > r_s'); -> c as r -> r_s+",
    ),
    "v_esc_dual": (
        "V_ESC_DUAL (dual escape velocity, coordinate)",
        "v_esc_dual = c*sqrt(r_s/r)",
        "coordinate; dual partner of V_DUAL under the redshift mapping",
        "r > 0; subluminal for r > r_s",
    ),
    "v_local": (
        "V_LOCAL (local energy-budget fall velocity)",
        "v_local = c*beta(r), beta = sqrt(Xi(2+Xi))/(1+Xi)",
        "local static-observer orthonormal frame; subluminal for all r > 0",
        "all r > 0 where Xi is defined",
    ),
    "v_buch": (
        "V_BUCH (book worked-example velocity)",
        "v_buch = c/sqrt(1 + Xi(r))",
        "coordinate expression from the book's Z.9368 worked example; NOT "
        "implemented in the original code base, NOT part of the duality",
        "all r > 0 where Xi is defined",
    ),
    "v_segment": (
        "V_SEGMENT (segment-structure progression rate, qualitative)",
        "no formula in corpus — 'inward progression rate of the segmental "
        "structure' (Metrik Z.209); local c stays c (Z.212); V_SEGMENT_LIMIT "
        "records the only quantitative statement",
        "not definable without a transport law (Lino-Audit C3: OPEN)",
        "qualitative only; no domain where a formula exists",
    ),
    "v_newton": (
        "V_NEWTON (Newtonian infall speed, Additive Decomposition)",
        "v_newton = sqrt(2GM/r)",
        "Newtonian local infall speed; SAME expression as V_ESC_DUAL but "
        "different name and radially inverted usage vs. V_DUAL "
        "('As v_fall decreases, segmentation relaxes')",
        "r > 0, weak-field Newtonian interpretation",
    ),
}

V_DUAL = "V_DUAL"
V_ESC_DUAL = "V_ESC_DUAL"
V_LOCAL = "V_LOCAL"
V_BUCH = "V_BUCH"
V_SEGMENT_LIMIT = "V_SEGMENT_LIMIT"
V_NEWTON = "V_NEWTON"


# ============================================================================
# IMPLEMENTATIONS
# ============================================================================

def v_dual(r: ArrayLike, M: float) -> ArrayLike:
    """V_DUAL = c*sqrt(r/r_s), valid r > r_s (Dual Velocities paper)."""
    r_arr = np.asarray(r, dtype=float)
    r_s = characteristic_radius(M)
    out = C * np.sqrt(r_arr / r_s)
    return float(out) if r_arr.ndim == 0 else out


def v_esc_dual(r: ArrayLike, M: float) -> ArrayLike:
    """V_ESC_DUAL = c*sqrt(r_s/r)."""
    r_arr = np.asarray(r, dtype=float)
    r_s = characteristic_radius(M)
    out = C * np.sqrt(r_s / r_arr)
    return float(out) if r_arr.ndim == 0 else out


def v_local(r: ArrayLike, M: float) -> ArrayLike:
    """V_LOCAL = c*beta(r) — identical to kinematics.v_fall (code standard)."""
    xi = xi_canonical(r, M)
    beta = np.sqrt(np.maximum(xi * (2.0 + xi), 0.0)) / (1.0 + xi)
    out = C * beta
    return float(out) if np.ndim(out) == 0 else out


def v_buch(r: ArrayLike, M: float) -> ArrayLike:
    """V_BUCH = c/sqrt(1+Xi(r)) — book worked example only (Z.9368)."""
    xi = xi_canonical(r, M)
    out = C / np.sqrt(1.0 + xi)
    return float(out) if np.ndim(out) == 0 else out


def v_newton(r: ArrayLike, M: float) -> ArrayLike:
    """V_NEWTON = sqrt(2GM/r) — Additive Decomposition naming (Z.76)."""
    r_arr = np.asarray(r, dtype=float)
    out = np.sqrt(2.0 * G * M / r_arr)
    return float(out) if r_arr.ndim == 0 else out


# ============================================================================
# E2: IDENTITY TESTS — book vs. papers vs. code
# ============================================================================

def dual_product_identity_residual(r: ArrayLike, M: float) -> ArrayLike:
    """
    E2 identity: v_esc_dual(r) * v_dual(r) = c^2 EXACTLY for r > r_s.

    This is an algebraic identity of the dual parametrization, verified
    numerically as a regression guard. It is explicitly NOT a field equation
    (Lino-Audit C1; primary text: dual relation from equating redshift
    factors, no dynamics).
    """
    return v_esc_dual(r, M) * v_dual(r, M) - C ** 2


def identity_test_report(M: float = 1.0, n: int = 200) -> dict:
    """
    E2 verification battery: book vs. papers vs. code.

    Checks (all purely algebraic/numerical, no model change):
      I1  dual product identity residual == 0 for r in (r_s, 20 r_s)
      I2  V_LOCAL(r_s) matches the documented code value 0.831832*c
      I3  V_ESC_DUAL-v_local cross-check at r_s: v_esc_dual(r_s)=c vs.
          code v_escape(r_s)=1.202166*c — the documented paper/code naming
          divergence (belegt in SSZ_VFALL_DEFINITIONS_AUDIT_V1)
      I4  book Z.9368 worked example at the photon sphere r=1.5 r_s:
          strong-variant v_buch = c/sqrt(1+Xi_strong) = 0.776c (this is what
          the code's regime routing produces), weak-variant c/sqrt(4/3) =
          0.866c (uses Xi_weak outside its domain x>2.2 — documented
          Code-vs-Buch inconsistency)
      I5  V_NEWTON == V_ESC_DUAL expression-wise (same formula, diff. name):
          v_newton(r, M) == v_esc_dual(r, M) for all r > 0
      I6  V_DUAL superluminal strictly outside r_s, equals c at r_s (limit)
    """
    r_s = characteristic_radius(M)
    rs_grid = r_s * np.linspace(1.0 + 1e-9, 20.0, n)

    # I1: dual product identity
    resid = dual_product_identity_residual(rs_grid, M)
    i1_max = float(np.max(np.abs(resid))) / C**2

    # I2: code value at r_s
    v_loc_rs = float(v_local(r_s, M)) / C

    # I3: naming divergence at r_s
    v_esc_code_rs = C / float(np.sqrt(np.maximum(
        1.0 - 1.0 / (1.0 + float(xi_canonical(r_s, M)))**2, 1e-300)))
    v_esc_code_rs /= C
    v_esc_dual_rs = float(v_esc_dual(r_s, M)) / C

    # I4: book worked example at the photon sphere r = 1.5 r_s
    x_ph = 1.5
    xi_weak_ph = 1.0 / (2.0 * x_ph)                     # 1/3 (weak formula)
    xi_strong_ph = 1.0 - np.exp(-1.618033988749895 / x_ph)  # Xi_strong
    v_buch_weak = 1.0 / np.sqrt(1.0 + xi_weak_ph)       # book: 0.866c
    v_buch_strong = 1.0 / np.sqrt(1.0 + xi_strong_ph)   # book: 0.776c
    v_buch_code = float(v_buch(x_ph * r_s, M)) / C      # code routing: strong

    # I5: same-expression check
    rng = r_s * np.linspace(0.5, 50.0, n)
    i5_max = float(np.max(np.abs(
        v_newton(rng, M) - v_esc_dual(rng, M)))) / C

    # I6: dual superluminality outside r_s
    outside = v_dual(r_s * np.linspace(1.0 + 1e-9, 10.0, n), M) / C
    i6_ok = bool(np.all(outside > 1.0))

    return {
        "I1_dual_product_max_residual_over_c2": i1_max,
        "I1_pass": i1_max < 1e-12,
        "I2_v_local_at_rs_over_c": v_loc_rs,
        "I2_pass": abs(v_loc_rs - 0.831832) < 1e-3,
        "I3_v_esc_code_at_rs_over_c": v_esc_code_rs,
        "I3_v_esc_dual_at_rs_over_c": v_esc_dual_rs,
        "I3_pass": abs(v_esc_code_rs - 1.202166) < 1e-3 and abs(v_esc_dual_rs - 1.0) < 1e-9,
        "I4_v_buch_weak_at_photon_sphere": float(v_buch_weak),
        "I4_v_buch_strong_at_photon_sphere": float(v_buch_strong),
        "I4_v_buch_code_at_photon_sphere": v_buch_code,
        "I4_pass": abs(v_buch_weak - 0.866025) < 1e-3
                   and abs(v_buch_strong - 0.776) < 5e-3
                   and abs(v_buch_code - float(v_buch_strong)) < 1e-9,
        "I5_newton_equals_esc_dual_max_diff_over_c": i5_max,
        "I5_pass": i5_max < 1e-12,
        "I6_dual_superluminal_outside_rs": i6_ok,
        "M": M, "n_grid": n,
    }

