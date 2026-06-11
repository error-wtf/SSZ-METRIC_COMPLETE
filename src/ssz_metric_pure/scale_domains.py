"""
SSZ Scale Domains Registry

Defines the seven canonical physical and mathematical scale domains of the
multi-scale Segmented Spacetime (SSZ) framework.

© 2025 Carmen N. Wrede & Lino Casu
Licensed under the Anti-Capitalist Software License v1.4
"""

SCALE_DOMAINS = {
    "PLANCK_FINE_STRUCTURE": {
        "name": "Planck & Fine-Structure Adjacent Scale",
        "physical_scale": "Planck length (l_P) and fine-structure scale (alpha)",
        "primary_quantities": ["PHI", "alpha_SSZ"],
        "required_formulas": ["phi_constant()", "alpha_reference()", "fine_structure_proxy()"],
        "valid_methods": ["XI_STRONG_FIELD_DIAGNOSTIC"],
        "implemented_functions": ["phi_constant", "alpha_reference", "fine_structure_proxy", "planck_scale_context"],
        "test_file": "tests/test_fine_structure_domain.py",
        "limitations": "Does not by itself prove a complete theory of quantum gravity.",
        "validation_status": "internal identity tested"
    },
    "PHI_LATTICE_SEGMENTATION": {
        "name": "Phi-Lattice & Segmentation Scale",
        "physical_scale": "Segment distances (rho) and phi-lattice coordinates",
        "primary_quantities": ["Xi(r)", "segment_density", "segment_distance"],
        "required_formulas": ["phi_lattice_points()", "segment_index_from_radius()", "radius_from_segment_index()"],
        "valid_methods": ["XI_DIRECT", "XI_STRONG_FIELD_DIAGNOSTIC"],
        "implemented_functions": ["phi_lattice_points", "segment_index_from_radius", "radius_from_segment_index", "segment_density_profile", "segment_distance", "segment_count_proxy"],
        "test_file": "tests/test_phi_lattice_segmentation.py",
        "limitations": "Model-bound static lattice spacing representation.",
        "validation_status": "internal identity tested"
    },
    "QUANTUM_FREQUENCY_PHASE": {
        "name": "Quantum Frequency & Phase Transport Scale",
        "physical_scale": "Wave phase accumulation and clock rate comparisons",
        "primary_quantities": ["D(r)", "s(r)", "local_c"],
        "required_formulas": ["local_c_invariance_check()", "frequency_ratio_from_D()", "wavelength_ratio_from_s()", "phase_path_integral()"],
        "valid_methods": ["XI_DIRECT", "SSZ_KINEMATIC_IDENTITY"],
        "implemented_functions": ["local_c_invariance_check", "frequency_ratio_from_D", "wavelength_ratio_from_s", "phase_path_integral", "frequency_curvature_proxy", "clock_ratio"],
        "test_file": "tests/test_phase_frequency_domain.py",
        "limitations": "Neglects wave dispersion in inhomogeneous non-vacuum matter fields.",
        "validation_status": "forward formula tested"
    },
    "ELECTROMAGNETIC_CLOCK": {
        "name": "Electromagnetic & Clock Observables Scale",
        "physical_scale": "Gravitational redshift, time dilation, and field scaling",
        "primary_quantities": ["D(r)", "s(r)", "electric_scaling", "magnetic_scaling"],
        "required_formulas": ["time_dilation_D()", "redshift_static()", "gps_clock_proxy()", "scale_electric_field()", "scale_magnetic_field()"],
        "valid_methods": ["XI_DIRECT", "PPN_COMPLETION"],
        "implemented_functions": ["time_dilation_D", "redshift_static", "gps_clock_proxy", "radial_scaling_factor", "scale_electric_field", "scale_magnetic_field", "light_travel_time_correction"],
        "test_file": "tests/test_em_clock_domain.py",
        "limitations": "Requires spherical symmetry; does not account for Earth's non-spherical quadrupole moments.",
        "validation_status": "external reference formula tested"
    },
    "WEAK_FIELD_PPN": {
        "name": "Weak-Field Parameterized Post-Newtonian (PPN) Scale",
        "physical_scale": "Solar System and astrophysical weak-field bounds",
        "primary_quantities": ["beta_PPN", "gamma_PPN"],
        "required_formulas": ["ppn_gamma()", "ppn_beta()", "lensing_deflection_ppn()", "shapiro_delay_ppn()", "perihelion_precession_ppn()"],
        "valid_methods": ["PPN_COMPLETION", "PPN_ORBIT"],
        "implemented_functions": ["ppn_gamma", "ppn_beta", "lensing_deflection_ppn", "shapiro_delay_ppn", "perihelion_precession_ppn"],
        "test_file": "tests/test_weak_field_ppn_domain.py",
        "limitations": "First-order weak field expansion only.",
        "validation_status": "external reference formula tested"
    },
    "STRONG_FIELD_COMPACT": {
        "name": "Strong-Field & Compact Object Scale",
        "physical_scale": "Photon sphere, event horizons, and core diagnostics",
        "primary_quantities": ["Xi(r_s)", "D_horizon", "energy_conditions"],
        "required_formulas": ["Xi_at_schwarzschild_radius()", "D_at_schwarzschild_radius()", "strong_field_regime_report()"],
        "valid_methods": ["XI_STRONG_FIELD_DIAGNOSTIC"],
        "implemented_functions": ["Xi_at_schwarzschild_radius", "D_at_schwarzschild_radius", "strong_field_regime_report", "compactness_report", "finite_boundary_report", "energy_condition_regime"],
        "test_file": "tests/test_strong_field_compact_domain.py",
        "limitations": "Model evaluated as static proxy diagnostic rather than dynamic curvature collapse.",
        "validation_status": "internal identity tested"
    },
    "NEUTRON_STAR": {
        "name": "Neutron-Star Scale Domain",
        "physical_scale": "Relativistic compact matter stars",
        "primary_quantities": ["neutron_star_compactness", "neutron_star_redshift"],
        "required_formulas": ["neutron_star_compactness()", "neutron_star_regime()", "neutron_star_redshift_prediction()"],
        "valid_methods": ["XI_STRONG_FIELD_DIAGNOSTIC", "XI_DIRECT"],
        "implemented_functions": ["neutron_star_compactness", "neutron_star_regime", "neutron_star_redshift_prediction", "neutron_star_surface_D", "neutron_star_usecase_report"],
        "test_file": "tests/test_neutron_star_domain.py",
        "limitations": "No full nuclear equation of state or rotational de-sphericalisation model included.",
        "validation_status": "external observational validation pending"
    }
}


def get_scale_domain(domain_id: str) -> dict:
    """Retrieve metadata report for a given scale domain."""
    return SCALE_DOMAINS.get(domain_id)


def list_scale_domains() -> list:
    """Return all defined scale domain dictionaries."""
    return list(SCALE_DOMAINS.values())
