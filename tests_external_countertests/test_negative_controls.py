"""
Tests implementing strict negative controls to verify the gauntlet can fail as designed.

© 2026 Carmen N. Wrede & Lino Casu
Licensed under the Anti-Capitalist Software License v1.4
"""

import pytest
from ssz_metric_pure.external_exact_comparison import classify_countertest_result
from ssz_metric_pure.external_countertests import run_single_countertest


def test_negative_controls():
    # 1. missing path should result in SKIP
    d = {
        "dataset_id": "test_missing",
        "local_path": "non_existent.fits"
    }
    res = run_single_countertest(d, {}, "nicer_surface_redshift_proxy")
    assert res["status"] == "SKIP"
    
    # 2. same_dataset should classify as EXPLORATORY
    pred = {"value": 1.0}
    obs = {"value": 1.0, "comparison_mode": "EXACT_DERIVED_OBSERVABLE_MODE"}
    dataset_entry = {"model_dependency": "none", "allowed_for_canonical_gate": False}
    target_params = {"allowed_for_canonical_gate": False}
    
    res_exp = classify_countertest_result(pred, obs, dataset_entry, target_params)
    assert res_exp["status"] == "EXPLORATORY"
    
    # 3. Large deviation should result in FAIL
    pred_bad = {"value": 1.00005}
    res_fail = classify_countertest_result(pred_bad, obs, dataset_entry, {"allowed_for_canonical_gate": True})
    assert res_fail["status"] == "FAIL"
