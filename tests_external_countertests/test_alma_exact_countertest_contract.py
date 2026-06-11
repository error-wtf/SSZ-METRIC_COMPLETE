"""
Tests for ALMA exact countertest contract.
"""
import pytest
from ssz_metric_pure.external_countertests import run_single_countertest

def test_alma_countertest():
    import tempfile
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        tmp.write(b"data")
        tmp_name = tmp.name
    try:
        d = {
            "dataset_id": "uid___A001_X12a_X3b",
            "target_name": "M87",
            "instrument": "ALMA",
            "observable_type": "alma_frequency_shift",
            "local_path": tmp_name,
            "data_level": "qa2",
            "validation_category": "standard",
            "limitations": ["none"]
        }
        target = {
            "mass_solar": 6.5e9,
            "allowed_for_canonical_gate": True,
            "independent_parameter_sources": [{"parameter": "mass", "source_type": "independent_literature"}],
            "limitations": ["none"]
        }
        res = run_single_countertest(d, target, "alma_frequency_shift")
        assert res["status"] in ["PASS_EXACT", "FAIL"]
    finally:
        import os
        if os.path.exists(tmp_name):
            os.remove(tmp_name)
