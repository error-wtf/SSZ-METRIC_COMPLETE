"""
SSZ Observable Registry Module

Defines the structured observable registry and its validation metadata under the
canonical Xi-primary forward-prediction framework.

© 2025 Carmen N. Wrede & Lino Casu
Licensed under the Anti-Capitalist Software License v1.4
"""

import json
import os

OBSERVABLE_REGISTRY = {
    "gps_clock_correction": {
        "id": "gps_clock_correction",
        "name": "GPS Clock General Relativistic Time Dilation Correction",
        "class": "TIMELIKE_STATIC",
        "method": "XI_DIRECT",
        "formula_source": "segment_density.md / time_dilation.md",
        "implementation_function": "predict_time_dilation",
        "input_parameters": {
            "r": 26560000.0,  # Orbit radius in meters
            "M": 5.972e24     # Earth mass in kg
        },
        "reference_value": 1.6697687676980877e-10,  # Fractional clock rate difference (GR prediction)
        "reference_uncertainty": 1.0e-14,
        "source_note": "Standard PPN / GR clock comparison on circular GPS orbit",
        "test_scope": "TIMELIKE_STATIC",
        "validation_type": "internal_formula_consistency",
        "fitting_allowed": False,
        "limitations": "Does not account for non-spherical Earth J2 or tidal perturbations."
    },
    "cassini_shapiro_gamma": {
        "id": "cassini_shapiro_gamma",
        "name": "Cassini Shapiro Delay PPN Completion Check",
        "class": "NULL_LIGHT",
        "method": "PPN_COMPLETION",
        "formula_source": "ppn_formulas.md / light_travel_time.md",
        "implementation_function": "predict_shapiro_ppn",
        "input_parameters": {
            "r_s": 2953.5,     # Sun Schwarzschild radius in meters
            "r1": 1.496e11,    # Earth-Sun distance (1 AU) in meters
            "r2": 1.433e12,    # Saturn-Sun distance in meters
            "d": 1.391e9,      # Solar diameter in meters (impact parameter proxy)
            "gamma_ppn": 1.0
        },
        "reference_value": 0.00025618146952174035,  # Logarithmic Shapiro delay contribution in seconds
        "reference_uncertainty": 1.0e-9,
        "source_note": "Cassini solar conjunction Shapiro delay measurement limit",
        "test_scope": "NULL_LIGHT",
        "validation_type": "internal_formula_consistency",
        "fitting_allowed": False,
        "limitations": "Neglects solar corona plasma delay contribution."
    },
    "mercury_perihelion": {
        "id": "mercury_perihelion",
        "name": "Mercury Perihelion Precession PPN Orbit Check",
        "class": "TIMELIKE_ORBIT",
        "method": "PPN_ORBIT",
        "formula_source": "ppn_formulas.md",
        "implementation_function": "predict_perihelion_ppn",
        "input_parameters": {
            "M": 1.989e30,      # Sun Mass in kg
            "a": 5.791e10,      # Semi-major axis in meters
            "e": 0.2056         # Eccentricity
        },
        "reference_value": 5.020005399568994e-07,  # Precession in radians per orbit
        "reference_uncertainty": 1.0e-11,
        "source_note": "Mercury perihelion precession from PPN metric orbit",
        "test_scope": "TIMELIKE_ORBIT",
        "validation_type": "internal_formula_consistency",
        "fitting_allowed": False,
        "limitations": "Requires full N-body PPN simulation for comparison to raw telemetry."
    },
    "eddington_lensing": {
        "id": "eddington_lensing",
        "name": "Eddington Solar Light Deflection Lensing Check",
        "class": "NULL_LIGHT",
        "method": "PPN_COMPLETION",
        "formula_source": "ppn_formulas.md",
        "implementation_function": "predict_lensing_ppn",
        "input_parameters": {
            "r_s": 2953.5,     # Sun Schwarzschild radius in meters
            "b": 696340000.0,  # Solar radius in meters (impact parameter)
            "gamma_ppn": 1.0
        },
        "reference_value": 8.4834e-6,  # Radian light deflection (1.75 arcseconds)
        "reference_uncertainty": 1.0e-8,
        "source_note": "1919 Eddington eclipse and modern VLBI lensing reference",
        "test_scope": "NULL_LIGHT",
        "validation_type": "internal_formula_consistency",
        "fitting_allowed": False,
        "limitations": "First-order PPN deflection only; neglects higher-order r_s^2/b^2 terms."
    },
    "static_redshift": {
        "id": "static_redshift",
        "name": "Pound-Rebka Gravitational Redshift",
        "class": "TIMELIKE_STATIC",
        "method": "XI_DIRECT",
        "formula_source": "time_dilation.md / frequency.py",
        "implementation_function": "predict_redshift",
        "input_parameters": {
            "r_emit": 6378100.0,       # Earth surface radius in meters
            "r_obs": 6378122.5,        # Receiver radius (22.5m altitude) in meters
            "M": 5.972e24              # Earth mass in kg
        },
        "reference_value": 2.44e-15,  # Fractional frequency shift (delta_f / f)
        "reference_uncertainty": 1.0e-17,
        "source_note": "Pound-Rebka tower experiment (1959)",
        "test_scope": "TIMELIKE_STATIC",
        "validation_type": "internal_formula_consistency",
        "fitting_allowed": False,
        "limitations": "Neglects local ground vibration and diurnal Earth rotation effects."
    },
    "dual_velocity_product": {
        "id": "dual_velocity_product",
        "name": "Orthonormal Escape-Fall Velocity Product Identity",
        "class": "KINEMATIC_INVARIANT",
        "method": "SSZ_KINEMATIC_IDENTITY",
        "formula_source": "dual_velocities.md / kinematics.py",
        "implementation_function": "predict_dual_velocity_product",
        "input_parameters": {
            "r": 1.0e7,         # Radius in meters
            "M": 5.972e24       # Earth mass in kg
        },
        "reference_value": 8.987551787368176e16,  # c^2 in m^2/s^2
        "reference_uncertainty": 0.0,
        "source_note": "Fundamental local conservation identity for canonical SSZ core",
        "test_scope": "KINEMATIC_INVARIANT",
        "validation_type": "internal_formula_consistency",
        "fitting_allowed": False,
        "limitations": "Identity is exact in static diagonal frame."
    },
    "finite_horizon_D": {
        "id": "finite_horizon_D",
        "name": "Regularized Horizon Dilation Limit Check",
        "class": "STRONG_FIELD_DIAGNOSTIC",
        "method": "XI_STRONG_FIELD_DIAGNOSTIC",
        "formula_source": "segment_density.md / strong_field.py",
        "implementation_function": "predict_finite_horizon_values",
        "input_parameters": {
            "M": 1.989e30       # Sun Mass in kg (test proxy)
        },
        "reference_value": 0.55502,  # 1 / (1 + Xi_strong(r_s)) ≈ 1 / (2 - e^-phi)
        "reference_uncertainty": 1.0e-5,
        "source_note": "Core regularization limit at characteristic radius r_s",
        "test_scope": "STRONG_FIELD_DIAGNOSTIC",
        "validation_type": "internal_formula_consistency",
        "fitting_allowed": False,
        "limitations": "Diagnostic of strong field regular core; observational values are pending."
    },
    "energy_condition_regime": {
        "id": "energy_condition_regime",
        "name": "Weak and Strong Energy Condition Diagnostics",
        "class": "STRONG_FIELD_DIAGNOSTIC",
        "method": "XI_STRONG_FIELD_DIAGNOSTIC",
        "formula_source": "energy_conditions.md / energy.py",
        "implementation_function": "predict_energy_condition_diagnostic",
        "input_parameters": {
            "r": 2.0e4,         # Radius in meters (neutron star domain)
            "M": 1.989e30       # Mass in kg (1 solar mass)
        },
        "reference_value": 1.0,  # 1.0 indicates both WEC and SEC are satisfied
        "reference_uncertainty": 0.0,
        "source_note": "Energy condition checks within regularized core",
        "test_scope": "STRONG_FIELD_DIAGNOSTIC",
        "validation_type": "internal_formula_consistency",
        "fitting_allowed": False,
        "limitations": "Evaluates effective matter fields as proxy; not a full physicalMatter source."
    },
    "light_travel_time_correction": {
        "id": "light_travel_time_correction",
        "name": "Light Travel Time Radial Gravity Correction",
        "class": "NULL_LIGHT",
        "method": "PPN_COMPLETION",
        "formula_source": "light_travel_time.md",
        "implementation_function": "predict_light_travel_time_correction",
        "input_parameters": {
            "r1": 1.0e7,        # Emit radius in meters
            "r2": 2.0e7,        # Obs radius in meters
            "M": 5.972e24       # Earth mass in kg
        },
        "reference_value": 1.0253898926239006e-11,  # Excess travel time in seconds
        "reference_uncertainty": 1.0e-20,
        "source_note": "Integrated excess light travel time under canonical SSZ",
        "test_scope": "NULL_LIGHT",
        "validation_type": "internal_formula_consistency",
        "fitting_allowed": False,
        "limitations": "Assumes strict radial null path propagation."
    }
}


def get_observable(obs_id):
    """Retrieve an observable by ID."""
    return OBSERVABLE_REGISTRY.get(obs_id)


def list_observables():
    """Return a list of all observable dictionary metadata."""
    return list(OBSERVABLE_REGISTRY.values())


def export_registry_to_json(filepath):
    """Serialize and export the registry to a json file."""
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(OBSERVABLE_REGISTRY, f, indent=4)
