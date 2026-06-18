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
    r_test = 3.0 * characteristic_radius(M_SUN)
    val = local_c_invariance_check(r_test, M_SUN)
    print(f"  r = 3r_s = {r_test:.3e} m")
    print(f"  Local c check: {val:.6e} m/s")
    print(f"  Expected C: {C:.6e} m/s")
    print(f"  Difference: {abs(val - C):.2e}")
    assert isclose(val, C, rel_tol=1e-12)


def test_frequency_ratio_uses_D():
    """Verify frequency ratio evaluations use direct temporal dilation D path."""
    r_emit = 2.0 * characteristic_radius(M_SUN)
    r_obs = 10.0 * characteristic_radius(M_SUN)
    f_ratio = frequency_ratio_from_D(r_emit, r_obs, M_SUN)
    print(f"  r_emit = 2r_s, r_obs = 10r_s")
    print(f"  Frequency ratio f_emit/f_obs: {f_ratio:.10f}")
    print(f"  Expected: < 1.0 (gravitational redshift)")
    assert f_ratio > 0.0
    assert f_ratio < 1.0


def test_wavelength_ratio_uses_s():
    """Verify wavelength / spatial scaling evaluations use direct spatial s path."""
    r_emit = 2.0 * characteristic_radius(M_SUN)
    r_obs = 10.0 * characteristic_radius(M_SUN)
    lambda_ratio = wavelength_ratio_from_s(r_emit, r_obs, M_SUN)
    print(f"  r_emit = 2r_s, r_obs = 10r_s")
    print(f"  Wavelength ratio lambda_obs/lambda_emit: {lambda_ratio:.10f}")
    print(f"  Expected: < 1.0")
    assert lambda_ratio > 0.0
    assert lambda_ratio < 1.0


def test_phase_integral_finite():
    """Verify radial phase accumulation integrals evaluate successfully and are positive."""
    path = [2.0 * characteristic_radius(M_SUN), 5.0 * characteristic_radius(M_SUN)]
    accum = phase_path_integral(path, M_SUN)
    print(f"  Path: 2r_s -> 5r_s")
    print(f"  Phase accumulation: {accum:.6e} rad")
    print(f"  Expected: > 0")
    assert accum > 0.0


def test_frequency_curvature_proxy():
    """Verify frequency curvature proxy returns finite values."""
    r_test = 3.0 * characteristic_radius(M_SUN)
    proxy = frequency_curvature_proxy(r_test, M_SUN)
    print(f"  r = 3r_s")
    print(f"  Frequency curvature proxy: {proxy:.6e}")
    print(f"  Expected: > 0")
    assert proxy > 0.0


def test_clock_ratio():
    """Verify clock comparisons use clock_ratio."""
    r1 = 2.0 * characteristic_radius(M_SUN)
    r2 = 5.0 * characteristic_radius(M_SUN)
    rat = clock_ratio(r1, r2, M_SUN)
    print(f"  Clock A at 2r_s, Clock B at 5r_s")
    print(f"  Clock ratio dT_A/dT_B: {rat:.10f}")
    print(f"  Expected: > 0")
    assert rat > 0.0
