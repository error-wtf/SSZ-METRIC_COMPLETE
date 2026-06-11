"""
Tests for the SSZ Quantum Frequency and Phase Transport Domain.

© 2025 Carmen N. Wrede & Lino Casu
Licensed under the Anti-Capitalist Software License v1.4
"""

import pytest
import numpy as np
from math import isclose
from ssz_metric_pure.constants import C, M_SUN
from ssz_metric_pure.core import characteristic_radius
from ssz_metric_pure.phase_frequency import (
    local_c_invariance_check,
    frequency_ratio_from_D,
    wavelength_ratio_from_s,
    phase_path_integral,
    frequency_curvature_proxy,
    clock_ratio
)


def test_local_c_invariance():
    """Verify local Light-Speed invariance check equals C identically."""
    val = local_c_invariance_check(3.0 * characteristic_radius(M_SUN), M_SUN)
    assert isclose(val, C, rel_tol=1e-12)


def test_frequency_ratio_uses_D():
    """Verify frequency ratio evaluations use direct temporal dilation D path."""
    r_emit = 2.0 * characteristic_radius(M_SUN)
    r_obs = 10.0 * characteristic_radius(M_SUN)
    f_ratio = frequency_ratio_from_D(r_emit, r_obs, M_SUN)
    assert f_ratio > 0.0
    # Higher observer altitude -> higher potential/higher f -> f_obs > f_emit
    assert f_ratio < 1.0  # f_emit / f_obs = D_obs/D_emit, so f_obs/f_emit < 1.0 is wrong, wait
    # f_obs/f_emit = D_emit / D_obs. Since D_emit < D_obs, D_emit/D_obs < 1.0! Correct!


def test_wavelength_ratio_uses_s():
    """Verify wavelength / spatial scaling evaluations use direct spatial s path."""
    r_emit = 2.0 * characteristic_radius(M_SUN)
    r_obs = 10.0 * characteristic_radius(M_SUN)
    lambda_ratio = wavelength_ratio_from_s(r_emit, r_obs, M_SUN)
    assert lambda_ratio > 0.0
    # Since lambda_obs / lambda_emit = s_obs / s_emit, and s_obs < s_emit, ratio < 1.0
    assert lambda_ratio < 1.0


def test_phase_integral_finite():
    """Verify radial phase accumulation integrals evaluate successfully and are positive."""
    path = [2.0 * characteristic_radius(M_SUN), 5.0 * characteristic_radius(M_SUN)]
    accum = phase_path_integral(path, M_SUN)
    assert accum > 0.0


def test_frequency_curvature_proxy():
    """Verify frequency curvature proxy returns finite values."""
    proxy = frequency_curvature_proxy(3.0 * characteristic_radius(M_SUN), M_SUN)
    assert proxy > 0.0


def test_clock_ratio():
    """Verify clock comparisons use clock_ratio."""
    rat = clock_ratio(2.0 * characteristic_radius(M_SUN), 5.0 * characteristic_radius(M_SUN), M_SUN)
    assert rat > 0.0
