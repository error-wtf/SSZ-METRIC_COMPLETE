"""
SSZ Observable Validation Layer

Executes the dynamic evaluation and validation of registered observables
against canonical Xi-primary SSZ core predictions.

Strictly enforces the Prime Directive routing and the forward/anti-circular protocol.

© 2025 Carmen Wrede & Lino Casu
Licensed under the Anti-Capitalist Software License v1.4
"""

import numpy as np
from .observable_registry import list_observables
from . import observable_predictions


def evaluate_observable_prediction(obs: dict) -> float:
    """
    Dynamically resolve and call the correct prediction function in
    observable_predictions.py with the input parameters provided.
    """
    func_name = obs["implementation_function"]
    func = getattr(observable_predictions, func_name, None)
    if not func:
        raise AttributeError(f"Prediction function '{func_name}' not found in observable_predictions.py")
    
    params = obs["input_parameters"]
    # Handle single positional parameters or keyword arguments
    # We dynamically pass the dictionary keys as keyword arguments
    return float(func(**params))


def validate_observable(obs: dict, rtol: float = 1e-3, atol: float = 1e-12) -> dict:
    """
    Validate a single registered observable against its reference value.
    Separates internal mathematical consistency from pending external references.
    """
    prediction = evaluate_observable_prediction(obs)
    ref_val = obs["reference_value"]
    val_type = obs["validation_type"]
    
    is_close = np.isclose(prediction, ref_val, rtol=rtol, atol=atol)
    
    # Absolute difference
    diff = abs(prediction - ref_val)
    
    status = "PASS" if is_close else "FAIL"
    if val_type == "external_reference_pending":
        status = "PENDING"
        
    return {
        "id": obs["id"],
        "name": obs["name"],
        "class": obs["class"],
        "method": obs["method"],
        "prediction": prediction,
        "reference_value": ref_val,
        "difference": diff,
        "validation_type": val_type,
        "status": status,
        "source_note": obs["source_note"]
    }


def run_full_validation_suite() -> dict:
    """
    Execute validation for all registered observables.
    Separates results into internal consistency, external references, and exploratory items.
    """
    results = []
    summary = {
        "PASS": 0,
        "FAIL": 0,
        "PENDING": 0,
        "total": 0
    }
    
    for obs in list_observables():
        res = validate_observable(obs)
        results.append(res)
        summary[res["status"]] += 1
        summary["total"] += 1
        
    return {
        "results": results,
        "summary": summary
    }
