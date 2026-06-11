"""
Highly Rigorous Whole-SSZ System Architecture Test.

Verifies:
- The entire multi-layered Segmented Spacetime (SSZ) stack is fully integrated and consistent.
- Primary segment density fields correctly generate the metric tensor, which in turn
  feeds the kinematics, electromagnetism, post-Newtonian, strong-field, energy,
  frequency, and falsification modules.
- No-freeze connection/curvature solvers and repository consistency validators
  guarantee the strict purity of the codebase.

© 2025 Carmen N. Wrede & Lino Casu
Licensed under the Anti-Capitalist Software License v1.4
"""

import pytest
import numpy as np
from pathlib import Path
from math import isclose
from ssz_metric_pure import (
    characteristic_radius,
    segment_density,
    D_from_xi,
    s_from_xi,
    metric_diagonal,
    coordinate_light_speed,
    effective_refractive_index,
    phase_velocity_ratio,
    beta_ppn_parameter,
    gamma_ppn_parameter,
    weak_field_expansion_coeffs,
    photon_sphere_radius,
    strong_field_redshift_limit,
    check_weak_energy_condition,
    check_strong_energy_condition,
    clock_comparison_ratio,
    phase_accumulation_radial,
    solar_system_ppn_limit_check,
    verify_light_deflection_bound,
    verify_core_purity,
    # New architecture-specific functions
    dual_velocity_product,
    light_travel_time_correction,
    ppn_gamma,
    ppn_beta,
    Xi_at_schwarzschild_radius,
    Xi_at_characteristic_radius,
    energy_condition_report,
    frequency_ratio,
    validate_core_identities,
    known_limitations,
    M_SUN,
    C,
    PHI
)


def test_whole_ssz_architecture_integration():
    """Verify that all architectural layers of the Whole-SSZ system operate in perfect unison."""
    r_s = characteristic_radius(M_SUN)
    
    # 1. Core layer -> Metric layer
    r_val = 3.0 * r_s
    xi_val = segment_density(r_val, M_SUN)
    D_val = D_from_xi(xi_val)
    s_val = s_from_xi(xi_val)
    
    g = metric_diagonal((1.0, r_val, np.pi/2.0, 0.0), M_SUN)
    assert isclose(g[0, 0], -(D_val ** 2) * (C ** 2))
    assert isclose(g[1, 1], s_val ** 2)
    
    # 2. Kinematics & Electromagnetism layers
    coord_c = coordinate_light_speed(r_val, M_SUN)
    n_index = effective_refractive_index(r_val, M_SUN)
    v_phase_ratio = phase_velocity_ratio(r_val, M_SUN)
    
    assert isclose(coord_c, C * (D_val ** 2))
    assert isclose(n_index, s_val / D_val)
    assert isclose(v_phase_ratio, D_val / s_val)
    assert isclose(coord_c, C / n_index)
    
    # 3. Post-Newtonian (PPN) layer
    assert beta_ppn_parameter() == 1.0
    assert gamma_ppn_parameter() == 1.0
    assert ppn_gamma() == 1.0
    assert ppn_beta() == 1.0
    
    coeffs = weak_field_expansion_coeffs(100.0 * r_s, M_SUN)
    assert coeffs["U"] == r_s / (2.0 * (100.0 * r_s))
    assert coeffs["g_tt_coeff_order1"] == -2.0
    
    # 4. Strong Field layer
    r_photon = photon_sphere_radius(M_SUN)
    assert isclose(r_photon, 3.0 * r_s)
    
    z_limit = strong_field_redshift_limit(M_SUN)
    xi_rs = segment_density(r_s, M_SUN)
    assert isclose(z_limit, 1.0 + xi_rs)
    
    # 5. Energy Conditions layer
    assert check_weak_energy_condition(r_val, M_SUN) is True
    assert check_strong_energy_condition(r_val, M_SUN) is True
    
    # 6. Frequency layer
    clock_ratio = clock_comparison_ratio(2.0 * r_s, 5.0 * r_s, M_SUN)
    D2 = D_from_xi(segment_density(2.0 * r_s, M_SUN))
    D5 = D_from_xi(segment_density(5.0 * r_s, M_SUN))
    assert isclose(clock_ratio, D5 / D2)
    
    # 7. Falsification & constraints layer
    assert solar_system_ppn_limit_check(M_SUN) is True
    assert verify_light_deflection_bound(100.0 * r_s, M_SUN, (2.0 * r_s) / (100.0 * r_s)) is True
    
    # 8. Repository consistency verification (ensuring strict package purity on the filesystem)
    assert verify_core_purity() is True


def test_specific_lino_function_existence():
    """Verify specific functions specified by Lino exist and act appropriately."""
    # Test kinematics dual velocity invariant
    p = dual_velocity_product(5.0 * characteristic_radius(M_SUN), M_SUN)
    assert isclose(p, C ** 2, rel_tol=1e-12)
    
    # Test electromagnetism light travel time correction
    dt = light_travel_time_correction(2.0 * characteristic_radius(M_SUN), 5.0 * characteristic_radius(M_SUN), M_SUN)
    assert dt > 0.0
    
    # Test strong field Schwarzschild radius / characteristic radius values
    v1 = Xi_at_schwarzschild_radius(M_SUN)
    v2 = Xi_at_characteristic_radius(M_SUN)
    assert isclose(v1, v2)
    assert isclose(v1, 1.0 - np.exp(-PHI), rel_tol=1e-12)
    
    # Test energy condition report
    rep = energy_condition_report(3.0 * characteristic_radius(M_SUN), M_SUN)
    assert rep["weak_energy_condition"] is True
    assert rep["status"] == "PASS"
    
    # Test frequency ratio
    f_rat = frequency_ratio(2.0 * characteristic_radius(M_SUN), 5.0 * characteristic_radius(M_SUN), M_SUN)
    assert f_rat > 0.0
    
    # Test validation of core identities
    assert validate_core_identities(3.0 * characteristic_radius(M_SUN), M_SUN) is True
    
    # Test falsification limitations
    lims = known_limitations()
    assert "nonlinear_stability" in lims


def test_essential_documentation_and_script_existence():
    """Verify that critical repo-perfection files exist."""
    repo_root = Path(__file__).resolve().parent.parent
    
    # Verify documentation files
    assert (repo_root / "REPRODUCIBILITY.md").exists()
    assert (repo_root / "docs/SSZ_DOCUMENTATION_TRACEABILITY.md").exists()
    assert (repo_root / "FINAL_INTEGRITY_REPORT.md").exists()
    assert (repo_root / "README.md").exists()
    
    # Verify install scripts
    assert (repo_root / "install.sh").exists()
    assert (repo_root / "install.bat").exists()
    assert (repo_root / "install.ps1").exists()
    
    # Verify pyproject.toml matches expected package
    pyproj_content = (repo_root / "pyproject.toml").read_text(encoding="utf-8")
    assert "ssz_metric_pure" in pyproj_content
