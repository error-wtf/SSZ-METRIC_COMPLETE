"""
Tests for checking external forward and anti-circularity constraints.

© 2026 Carmen N. Wrede & Lino Casu
Licensed under the Anti-Capitalist Software License v1.4
"""

import os
import pytest
from ssz_metric_pure.nicer_validation import compare_nicer_prediction
from ssz_metric_pure.alma_validation import compare_alma_prediction


def test_anticircularity_model_dependency_status():
    """Verify that entries with high model dependency return WARN/FAIL and anti_circularity=FAIL."""
    entry_high = {
        "dataset_id": "high_dep_test",
        "target_name": "PSR High",
        "model_dependency": "high",
        "validation_category": "raw_data",
        "limitations": ["high dependency on GR posteriors"]
    }
    prediction = {"observable_type": "redshift", "value": 0.1}
    derived = {"observable_type": "redshift", "value": 0.2, "uncertainty": 0.01}  # Large gap
    
    comp_nicer = compare_nicer_prediction(entry_high, prediction, derived)
    assert comp_nicer["status"] in ["WARN", "FAIL"]
    assert comp_nicer["anti_circularity"] == "FAIL"
    
    comp_alma = compare_alma_prediction(entry_high, prediction, derived)
    assert comp_alma["status"] in ["WARN", "FAIL"]
    assert comp_alma["anti_circularity"] == "FAIL"


def test_no_fitting_in_external_validation():
    """Verify that banned fitting terms are completely absent from the source code."""
    banned_terms = [
        "curve_fit", "least_squares", "polyfit", "linregress",
        "differential_evolution", "lmfit", "sklearn", "tune_to_data",
        "optimize_to_match", "calibrate_from_observed"
    ]
    
    source_dirs = [
        "src/ssz_metric_pure/external_data.py",
        "src/ssz_metric_pure/nicer_validation.py",
        "src/ssz_metric_pure/alma_validation.py",
        "src/ssz_metric_pure/external_validation_report.py",
        "src/ssz_metric_pure/external_fetch_common.py",
        "src/ssz_metric_pure/nicer_fetch.py",
        "src/ssz_metric_pure/alma_fetch.py"
    ]
    
    for relative_path in source_dirs:
        abs_p = os.path.abspath(relative_path)
        if not os.path.exists(abs_p):
            continue
        with open(abs_p, "r", encoding="utf-8") as f:
            content = f.read()
            for term in banned_terms:
                assert term not in content, f"Banned fitting term '{term}' found in {relative_path}"
