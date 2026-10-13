"""
E1+E2 Tests: Velocity namespace separation and identity battery.

Verifies (no model change, no frozen artifact touched):
  - The six velocity quantities from the 25-paper corpus have unique
    symbols with documented frame/domain (E1).
  - The dual product v_esc_dual * v_dual = c^2 holds as an algebraic
    identity for r > r_s (E2-I1), and is NOT treated as a field equation.
  - The code's v_fall/v_escape match V_LOCAL / (V_ESC_DUAL naming
    divergence documented) (E2-I2/I3).
  - The book worked example (Z.9368) is reproducible via V_BUCH (E2-I4).
  - V_NEWTON and V_ESC_DUAL are the SAME expression under different names
    (E2-I5) — the radially-inverted-usage finding from the corpus audit.

© 2026 Carmen N. Wrede, Lino P. Casu & Bingsi
Licensed under the Anti-Capitalist Software License v1.4
"""

import numpy as np
import pytest

from ssz_metric_pure.constants import C
from ssz_metric_pure.core import characteristic_radius, xi_canonical
from ssz_metric_pure.kinematics import v_fall as code_v_fall
from ssz_metric_pure.kinematics import v_escape as code_v_escape
from ssz_metric_pure.velocity_namespace import (
    V_BUCH, V_DUAL, V_ESC_DUAL, V_LOCAL, V_NEWTON, V_SEGMENT_LIMIT,
    VELOCITY_NAMESPACE_DOC, dual_product_identity_residual, identity_test_report,
    v_buch, v_dual, v_esc_dual, v_local, v_newton,
)

M = 1.0
R_S = characteristic_radius(M)


# ============================================================================
# E1: namespace completeness
# ============================================================================

class TestE1Namespace:
    def test_all_six_documented(self):
        expected = {"v_dual", "v_esc_dual", "v_local", "v_buch", "v_segment", "v_newton"}
        assert set(VELOCITY_NAMESPACE_DOC.keys()) == expected

    def test_functional_roles_documented(self):
        # Lino-Go addendum: the two additional functional roles (Materie->Frequenz,
        # Singularitaet als Grenzflaeche max. Fallgeschwindigkeit) must be present
        # in the module source map — as interpretations, NOT as equations.
        import ssz_metric_pure.velocity_namespace as vnm
        src = vnm.__doc__ or ""
        assert "ROLE_FREQ" in src and "ROLE_SING" in src
        assert "matter transforms into frequency" in src or "frequency" in src
        assert "NOT be promoted" in src or "not be promoted" in src or "CRITICAL RULE" in src

    def test_each_entry_has_four_fields(self):
        for key, entry in VELOCITY_NAMESPACE_DOC.items():
            assert len(entry) == 4, f"{key}: name/def/frame/validity required"
            name, definition, frame, validity = entry
            for field in (name, definition, frame, validity):
                assert isinstance(field, str) and len(field) > 10

    def test_symbols_not_colliding(self):
        # distinct quantities must not silently share one symbol
        names = {entry[0] for entry in VELOCITY_NAMESPACE_DOC.values()}
        assert len(names) == 6

    def test_segment_flag_exists(self):
        # V_SEGMENT has no formula; the limit symbol documents that fact
        assert V_SEGMENT_LIMIT == "V_SEGMENT_LIMIT"


# ============================================================================
# E2: identity battery
# ============================================================================

class TestE2Identities:
    def test_I1_dual_product_identity(self):
        rep = identity_test_report(M=M, n=200)
        assert rep["I1_pass"], f"dual product residual too large: {rep}"

    def test_I1_grid_independent(self):
        r_grid = R_S * np.array([1.0 + 1e-6, 1.5, 2.0, 3.0, 10.0, 100.0])
        resid = dual_product_identity_residual(r_grid, M)
        assert np.allclose(resid, 0.0, atol=1e-8 * C**2)

    def test_I2_local_velocity_code_value(self):
        assert abs(v_local(R_S, M) / C - 0.831832) < 1e-3

    def test_I2b_v_local_equals_kinematics_v_fall(self):
        for r in [R_S * f for f in (1.1, 1.5, 2.0, 3.0, 10.0)]:
            assert abs(v_local(r, M) - code_v_fall(r, M)) < 1e-9 * C

    def test_I3_esc_code_vs_esc_dual_divergence_documented(self):
        rep = identity_test_report(M=M)
        # both sides of the documented divergence must be present
        assert rep["I3_pass"], (
            f"code v_escape(r_s)={rep['I3_v_esc_code_at_rs_over_c']:.6f}c "
            f"(expected 1.202166c), "
            f"v_esc_dual(r_s)={rep['I3_v_esc_dual_at_rs_over_c']:.6f}c "
            "(expected exactly 1.0c)"
        )

    def test_I4_buch_worked_example(self):
        rep = identity_test_report(M=M)
        # weak variant (out of domain, as printed in the book): 0.866c
        assert abs(rep["I4_v_buch_weak_at_photon_sphere"] - 0.866025) < 1e-3
        # strong variant (what the code routing actually produces): 0.776c
        assert abs(rep["I4_v_buch_strong_at_photon_sphere"] - 0.776) < 5e-3
        # code V_BUCH at 1.5 r_s must equal the strong variant exactly
        assert abs(rep["I4_v_buch_code_at_photon_sphere"]
                   - rep["I4_v_buch_strong_at_photon_sphere"]) < 1e-9

    def test_I5_newton_is_esc_dual_under_different_name(self):
        rep = identity_test_report(M=M)
        assert rep["I5_pass"]

    def test_I5b_newton_esc_dual_expression_identity(self):
        for r in [R_S * f for f in (0.5, 1.0, 2.0, 5.0, 20.0)]:
            assert abs(v_newton(r, M) - v_esc_dual(r, M)) < 1e-9 * C

    def test_I6_dual_superluminal_only_outside(self):
        r_grid = R_S * np.linspace(1.0 + 1e-9, 10.0, 50)
        assert np.all(v_dual(r_grid, M) / C > 1.0)

    def test_I6b_dual_equals_c_at_horizon_limit(self):
        # limit r -> r_s+: v_dual -> c (Z.204: 'v_fall ↓ c at the horizon')
        eps = 1e-10
        assert abs(v_dual(R_S * (1.0 + eps), M) / C - 1.0) < 1e-5

    def test_I7_additive_decomposition_frame_dependence_open(self):
        # Lino-Go E2 point 3: v_total = v_fall + v_eigen is galilean in the
        # corpus WITHOUT a transformation rule -> status stays OPEN. The only
        # testable consequence: V_LOCAL is subluminal everywhere on its domain,
        # so it cannot be the "v_fall" of a galilean split of physical velocities.
        rep = identity_test_report(M=M)
        assert rep["I7_pass"]
        assert rep["I7_v_local_max_over_c"] < 1.0
        assert "OPEN" in rep["I7_additive_decomposition_status"]

    def test_I8_segment_transport_lambda_is_not_EM(self):
        # Lino-Go E2 point 4: v_fall = lambda*f exists in the corpus as a
        # bookkeeping relation only; lambda is the SEGMENT-STRUCTURE wavelength
        # ("the wave must match local segment structure"), explicitly not the
        # EM wavelength of the radiowave carrier. No formula -> no numerics.
        rep = identity_test_report(M=M)
        assert rep["I8_pass"]
        assert rep["I8_segment_transport_status"] == "OPEN_no_transport_law_in_corpus"
        assert rep["I8_lambda_interpretation"] == (
            "segment_structure_wavelength_not_EM_wavelength")


# ============================================================================
# Corpus-consistency regression guards (pure numerics, no model change)
# ============================================================================

class TestCorpusRegression:
    def test_full_report_battery(self):
        rep = identity_test_report(M=1.0, n=400)
        for key in rep:
            if key.endswith("_pass"):
                assert rep[key], f"{key} failed: {rep}"

    def test_xi_unchanged(self):
        # guard: the canonical Xi must be untouched by E1/E2
        # (tolerance 1e-11: float noise in characteristic_radius, not a model change)
        assert abs(float(xi_canonical(R_S, M)) - 0.8017118471398135) < 1e-11
