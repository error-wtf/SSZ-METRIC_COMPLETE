"""
ssz_metric_pure - Canonical Pure Segmented Spacetime (SSZ) Metric Library

This is the official, unified, mathematically rigorous implementation of the pure
Segmented Spacetime (SSZ) core metric, based strictly on the ssz-complete-documentation
as the Single Source of Truth.

The segment density field Xi(r) is the primary physical field. All scaling factors,
rapidity factors, and metric components are derived directly from Xi.

No standard General Relativity or rotating scaffolds are imported or present in this package.

© 2025 Carmen Wrede & Lino Casu
Licensed under the Anti-Capitalist Software License v1.4
"""

__version__ = "1.1.0-canonical-pure"
__author__ = "Carmen Wrede & Lino Casu"

from .constants import (
    PHI,
    C,
    G,
    M_SUN,
    R_SUN,
    X_BLEND_MIN,
    X_BLEND_MAX,
)

from .core import (
    characteristic_radius,
    compactness_x,
    xi_weak,
    xi_strong,
    xi_blend,
    xi_canonical,
    D_from_xi,
    s_from_xi,
    gamma_from_xi,
    beta_from_gamma,
    regime_of_r,
)

from .segmentation import (
    segment_density,
    segment_scale,
    segment_distance,
    segment_count_proxy,
    local_orthonormal_speed_check,
)

from .metric import (
    metric_diagonal,
    inverse_metric_diagonal,
    det_metric_diagonal,
    metric_components,
    metric_flow_form,
)

from .tensor import (
    numerical_derivative_metric,
    christoffel_symbols,
    riemann_tensor,
    ricci_tensor,
    ricci_scalar,
    einstein_tensor,
    symbolic_curvature_diagonal,
)

from .observables import (
    ObservableClass,
    MethodAssignment,
    classify_observable,
    method_for_observable,
    SSZObservableSuite,
)

from .validation import (
    verify_algebraic_coupling,
    validate_core_identities,
)

from .kinematics import (
    coordinate_light_speed,
    free_fall_velocity_profile,
    dual_velocity_product,
)

from .electromagnetism import (
    effective_refractive_index,
    phase_velocity_ratio,
    light_travel_time_correction,
)

from .ppn import (
    beta_ppn_parameter,
    gamma_ppn_parameter,
    weak_field_expansion_coeffs,
    ppn_gamma,
    ppn_beta,
)

from .strong_field import (
    photon_sphere_radius,
    strong_field_redshift_limit,
    Xi_at_schwarzschild_radius,
    Xi_at_characteristic_radius,
)

from .energy import (
    check_weak_energy_condition,
    check_strong_energy_condition,
    energy_condition_report,
)

from .frequency import (
    clock_comparison_ratio,
    phase_accumulation_radial,
    frequency_ratio,
)

from .falsification import (
    solar_system_ppn_limit_check,
    verify_light_deflection_bound,
    known_limitations,
)

from .repo_consistency import (
    verify_core_purity,
)

from .observable_registry import (
    OBSERVABLE_REGISTRY,
    get_observable,
    list_observables,
    export_registry_to_json,
)

from .forward_protocol import (
    run_all_protocols,
    validate_no_fitting_used,
)

from .observable_predictions import (
    predict_time_dilation,
    predict_redshift,
    predict_light_travel_time_correction,
    predict_lensing_ppn,
    predict_shapiro_ppn,
    predict_perihelion_ppn,
    predict_dual_velocity_product,
    predict_finite_horizon_values,
    predict_energy_condition_diagnostic,
)

from .observable_validation import (
    run_full_validation_suite,
    validate_observable,
)

__all__ = [
    # Constants
    "PHI",
    "C",
    "G",
    "M_SUN",
    "R_SUN",
    "X_BLEND_MIN",
    "X_BLEND_MAX",
    
    # Core Potentials and Splines (Xi is Primary!)
    "characteristic_radius",
    "compactness_x",
    "xi_weak",
    "xi_strong",
    "xi_blend",
    "xi_canonical",
    "D_from_xi",
    "s_from_xi",
    "gamma_from_xi",
    "beta_from_gamma",
    "regime_of_r",
    
    # Physical Segmentation operations
    "segment_density",
    "segment_scale",
    "segment_distance",
    "segment_count_proxy",
    "local_orthonormal_speed_check",
    
    # Metric Implementations
    "metric_diagonal",
    "inverse_metric_diagonal",
    "det_metric_diagonal",
    "metric_components",
    "metric_flow_form",
    
    # Tensor Geometry Engine
    "numerical_derivative_metric",
    "christoffel_symbols",
    "riemann_tensor",
    "ricci_tensor",
    "ricci_scalar",
    "einstein_tensor",
    "symbolic_curvature_diagonal",
    
    # Observables Suite (Postulate 5 & Prime Directive)
    "ObservableClass",
    "MethodAssignment",
    "classify_observable",
    "method_for_observable",
    "SSZObservableSuite",
    
    # Validation helpers
    "verify_algebraic_coupling",
    "validate_core_identities",
    
    # Whole-SSZ Modules
    "coordinate_light_speed",
    "free_fall_velocity_profile",
    "dual_velocity_product",
    "effective_refractive_index",
    "phase_velocity_ratio",
    "light_travel_time_correction",
    "beta_ppn_parameter",
    "gamma_ppn_parameter",
    "ppn_gamma",
    "ppn_beta",
    "weak_field_expansion_coeffs",
    "photon_sphere_radius",
    "strong_field_redshift_limit",
    "Xi_at_schwarzschild_radius",
    "Xi_at_characteristic_radius",
    "check_weak_energy_condition",
    "check_strong_energy_condition",
    "energy_condition_report",
    "clock_comparison_ratio",
    "phase_accumulation_radial",
    "frequency_ratio",
    "solar_system_ppn_limit_check",
    "verify_light_deflection_bound",
    "known_limitations",
    "verify_core_purity",
    
    # Forward Observable Expansion Layer
    "OBSERVABLE_REGISTRY",
    "get_observable",
    "list_observables",
    "export_registry_to_json",
    "run_all_protocols",
    "validate_no_fitting_used",
    "predict_time_dilation",
    "predict_redshift",
    "predict_light_travel_time_correction",
    "predict_lensing_ppn",
    "predict_shapiro_ppn",
    "predict_perihelion_ppn",
    "predict_dual_velocity_product",
    "predict_finite_horizon_values",
    "predict_energy_condition_diagnostic",
    "run_full_validation_suite",
    "validate_observable",
]
