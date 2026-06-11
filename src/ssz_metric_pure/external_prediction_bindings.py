"""
SSZ External Prediction Bindings Module

Binds scale-domain observables to canonical core metric equations (Xi -> D, s -> g_munu)
in a strictly forward, non-circular fashion.

© 2026 Carmen N. Wrede & Lino Casu
Licensed under the Anti-Capitalist Software License v1.4
"""

from typing import Dict, Any, Optional
from .core import xi_canonical, D_from_xi, s_from_xi, characteristic_radius
from .electromagnetism import light_travel_time_correction


def predict_for_external_observable(
    observable_type: str,
    target_params: Dict[str, Any],
    dataset_entry: Dict[str, Any]
) -> Dict[str, Any]:
    """Route prediction request to correct SSZ scaling formula."""
    if observable_type == "nicer_surface_redshift_proxy":
        return predict_nicer_surface_redshift_proxy(target_params)
    elif observable_type == "nicer_clock_phase_proxy":
        return predict_nicer_clock_phase_proxy(target_params)
    elif observable_type == "alma_frequency_shift":
        return predict_alma_frequency_shift(target_params, dataset_entry)
    elif observable_type == "alma_line_velocity_proxy":
        return predict_alma_line_velocity_proxy(target_params, dataset_entry)
    elif observable_type == "alma_phase_path_integral":
        return predict_alma_phase_path_integral(target_params, dataset_entry)
    elif observable_type == "alma_light_travel_time":
        return predict_alma_light_travel_time(target_params, dataset_entry)
    else:
        raise ValueError(f"Unsupported observable prediction type: {observable_type}")


def predict_nicer_surface_redshift_proxy(target_params: Dict[str, Any]) -> Dict[str, Any]:
    """Compute surface gravitational redshift proxy z = Xi(R)."""
    M = target_params.get("mass_kg") or (target_params.get("mass_solar", 1.4) * 1.989e30)
    R = target_params.get("radius_m") or (target_params.get("radius_km", 12.0) * 1000.0)
    
    xi = xi_canonical(R, M)
    
    return {
        "prediction_id": "nicer_redshift_pred",
        "observable_type": "nicer_surface_redshift_proxy",
        "value": float(xi),
        "unit": "dimensionless",
        "formula_chain": ["Xi(r)", "D(r)=1/(1+Xi)", "z = Xi(R)"],
        "input_parameters": {"mass_kg": M, "radius_m": R},
        "no_fitting": True,
        "limitations": ["static spherical configuration only", "excludes rotational de-sphericalisation"]
    }


def predict_nicer_clock_phase_proxy(target_params: Dict[str, Any]) -> Dict[str, Any]:
    """Compute timing clock phase delay proxy derived from clock dilation ratio."""
    M = target_params.get("mass_kg") or (target_params.get("mass_solar", 1.4) * 1.989e30)
    R = target_params.get("radius_m") or (target_params.get("radius_km", 12.0) * 1000.0)
    
    xi = xi_canonical(R, M)
    D = D_from_xi(xi)
    
    return {
        "prediction_id": "nicer_clock_phase_pred",
        "observable_type": "nicer_clock_phase_proxy",
        "value": float(1.0 - D),
        "unit": "phase_ratio",
        "formula_chain": ["Xi(r)", "D(r)=1/(1+Xi)", "phase_delay = 1 - D"],
        "input_parameters": {"mass_kg": M, "radius_m": R},
        "no_fitting": True,
        "limitations": ["static clock comparison limits"]
    }


def predict_alma_frequency_shift(target_params: Dict[str, Any], dataset_entry: Dict[str, Any]) -> Dict[str, Any]:
    """Compute static frequency shift ratio z = D_obs/D_emit - 1."""
    M = target_params.get("mass_kg") or (target_params.get("mass_solar", 6.5e9) * 1.989e30)
    r_emit = target_params.get("r_emit_m") or (100.0 * characteristic_radius(M))
    r_obs = target_params.get("r_obs_m") or (1e6 * characteristic_radius(M))
    
    xi_emit = xi_canonical(r_emit, M)
    xi_obs = xi_canonical(r_obs, M)
    D_emit = D_from_xi(xi_emit)
    D_obs = D_from_xi(xi_obs)
    
    val = float((D_obs / D_emit) - 1.0)
    return {
        "prediction_id": "alma_freq_shift_pred",
        "observable_type": "alma_frequency_shift",
        "value": val,
        "unit": "dimensionless",
        "formula_chain": ["Xi(r)", "D(r)=1/(1+Xi)", "1+z = D_obs/D_emit"],
        "input_parameters": {"mass_kg": M, "r_emit_m": r_emit, "r_obs_m": r_obs},
        "no_fitting": True,
        "limitations": ["assumes static sender and receiver positioning"]
    }


def predict_alma_line_velocity_proxy(target_params: Dict[str, Any], dataset_entry: Dict[str, Any]) -> Dict[str, Any]:
    """Compute radial line velocity proxy incorporating spatial stretching s(r)."""
    M = target_params.get("mass_kg") or (target_params.get("mass_solar", 6.5e9) * 1.989e30)
    r = target_params.get("r_emit_m") or (100.0 * characteristic_radius(M))
    
    import numpy as np
    v_newt = np.sqrt(6.6743e-11 * M / r) if r > 0 else 0.0
    s_factor = s_from_xi(xi_canonical(r, M))
    val = float(v_newt * s_factor)
    
    return {
        "prediction_id": "alma_line_velocity_pred",
        "observable_type": "alma_line_velocity_proxy",
        "value": val,
        "unit": "m_s",
        "formula_chain": ["Xi(r)", "s(r)=1+Xi", "v_scaled = v_newt * s"],
        "input_parameters": {"mass_kg": M, "r_emit_m": r},
        "no_fitting": True,
        "limitations": ["assumes circular orbital path gas motion"]
    }


def predict_alma_phase_path_integral(target_params: Dict[str, Any], dataset_entry: Dict[str, Any]) -> Dict[str, Any]:
    """Compute phase integration proxy along specified coordinate pathways."""
    M = target_params.get("mass_kg") or (target_params.get("mass_solar", 6.5e9) * 1.989e30)
    r1 = target_params.get("r_emit_m") or (2.0 * characteristic_radius(M))
    r2 = target_params.get("r_obs_m") or (10.0 * characteristic_radius(M))
    
    import numpy as np
    r_vals = np.linspace(r1, r2, 100)
    xi_vals = xi_canonical(r_vals, M)
    n_vals = (1.0 + xi_vals) ** 2
    val = float(np.trapezoid(n_vals, r_vals))
    
    return {
        "prediction_id": "alma_phase_integral_pred",
        "observable_type": "alma_phase_path_integral",
        "value": val,
        "unit": "meters",
        "formula_chain": ["Xi(r)", "metric_components", "phase_integral = integral n dr"],
        "input_parameters": {"mass_kg": M, "r_start": r1, "r_end": r2},
        "no_fitting": True,
        "limitations": ["radial path integration only"]
    }


def predict_alma_light_travel_time(target_params: Dict[str, Any], dataset_entry: Dict[str, Any]) -> Dict[str, Any]:
    """Compute radial light travel time corrections."""
    M = target_params.get("mass_kg") or (target_params.get("mass_solar", 6.5e9) * 1.989e30)
    r1 = target_params.get("r_emit_m") or (2.0 * characteristic_radius(M))
    r2 = target_params.get("r_obs_m") or (10.0 * characteristic_radius(M))
    
    val = float(light_travel_time_correction(r1, r2, M))
    return {
        "prediction_id": "alma_light_travel_time_pred",
        "observable_type": "alma_light_travel_time",
        "value": val,
        "unit": "seconds",
        "formula_chain": ["Xi(r)", "s(r)=1+Xi", "D(r)=1/(1+Xi)", "excess_time = integral (s/D - 1) dr / c"],
        "input_parameters": {"mass_kg": M, "r_start": r1, "r_end": r2},
        "no_fitting": True,
        "limitations": ["assumes propagation along strictly radial null geodesics"]
    }
