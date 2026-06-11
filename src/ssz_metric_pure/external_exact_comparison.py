"""
SSZ External Exact Comparison Module

Provides comparison modes including EXACT_IDENTITY_MODE, EXACT_DERIVED_OBSERVABLE_MODE,
and OBSERVATIONAL_UNCERTAINTY_MODE to evaluate forward predictions.

© 2026 Carmen N. Wrede & Lino Casu
Licensed under the Anti-Capitalist Software License v1.4
"""

import math
from typing import Dict, Any


def compute_absolute_residual(prediction: Dict[str, Any], observable: Dict[str, Any]) -> float:
    """Calculate the absolute difference between predicted and derived values."""
    return float(abs(prediction["value"] - observable["value"]))


def compute_relative_residual(prediction: Dict[str, Any], observable: Dict[str, Any]) -> float:
    """Calculate the relative difference between predicted and derived values."""
    obs_val = abs(observable["value"])
    if obs_val < 1e-15:
        return float(abs(prediction["value"] - observable["value"]))
    return float(abs(prediction["value"] - observable["value"]) / obs_val)


def within_exact_tolerance(
    prediction: Dict[str, Any],
    observable: Dict[str, Any],
    abs_tol: float = 1e-12,
    rel_tol: float = 1e-10
) -> bool:
    """Check if residual meets exact strict numerical tolerances."""
    abs_res = compute_absolute_residual(prediction, observable)
    rel_res = compute_relative_residual(prediction, observable)
    return abs_res <= abs_tol or rel_res <= rel_tol


def compare_exact(
    prediction: Dict[str, Any],
    observable: Dict[str, Any],
    abs_tol: float = 1e-12,
    rel_tol: float = 1e-10
) -> Dict[str, Any]:
    """Execute exact numerical comparison, returning PASS_EXACT or FAIL status."""
    abs_res = compute_absolute_residual(prediction, observable)
    rel_res = compute_relative_residual(prediction, observable)
    passed = abs_res <= abs_tol or rel_res <= rel_tol
    return {
        "status": "PASS_EXACT" if passed else "FAIL",
        "absolute_residual": abs_res,
        "relative_residual": rel_res,
        "comparison_mode": "EXACT_DERIVED_OBSERVABLE_MODE" if observable.get("comparison_mode") != "EXACT_IDENTITY_MODE" else "EXACT_IDENTITY_MODE"
    }


def compare_uncertainty(prediction: Dict[str, Any], observable: Dict[str, Any]) -> Dict[str, Any]:
    """Compare predictions under standard observational uncertainty error bounds."""
    abs_res = compute_absolute_residual(prediction, observable)
    rel_res = compute_relative_residual(prediction, observable)
    sigma = observable.get("uncertainty")
    
    if sigma is None or sigma <= 0.0:
        return {
            "status": "WARN",
            "absolute_residual": abs_res,
            "relative_residual": rel_res,
            "message": "Uncertainty unavailable: downgraded to WARN status.",
            "comparison_mode": "OBSERVATIONAL_UNCERTAINTY_MODE"
        }
        
    nsigma = abs_res / sigma
    passed = nsigma <= 2.0
    status = "PASS_UNCERTAINTY" if passed else ("WARN" if nsigma <= 3.0 else "FAIL")
    return {
        "status": status,
        "absolute_residual": abs_res,
        "relative_residual": rel_res,
        "n_sigma": nsigma,
        "comparison_mode": "OBSERVATIONAL_UNCERTAINTY_MODE"
    }


def classify_countertest_result(
    prediction: Dict[str, Any],
    observable: Dict[str, Any],
    dataset_entry: Dict[str, Any],
    target_params: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Synthesizes and classifies predictions under strict anti-circularity guidelines.
    """
    mode = observable.get("comparison_mode") or dataset_entry.get("comparison_mode_preference") or "OBSERVATIONAL_UNCERTAINTY_MODE"
    
    # Check parameters
    dep = dataset_entry.get("model_dependency", "medium")
    allowed_hard = dataset_entry.get("allowed_for_canonical_gate", False) or target_params.get("allowed_for_canonical_gate", True)
    
    # Enforce exploratory restriction
    is_exploratory = (dep == "high") or (not allowed_hard)
    
    if mode in ["EXACT_IDENTITY_MODE", "EXACT_DERIVED_OBSERVABLE_MODE"]:
        res = compare_exact(prediction, observable)
        if is_exploratory and res["status"] == "PASS_EXACT":
            res["status"] = "EXPLORATORY"
        return res
    else:
        res = compare_uncertainty(prediction, observable)
        if is_exploratory and res["status"] in ["PASS_UNCERTAINTY", "WARN"]:
            res["status"] = "EXPLORATORY"
        return res
