"""
Tests for NICER exact countertest contract.
"""
import pytest
from ssz_metric_pure.external_countertests import run_single_countertest

def test_nicer_countertest():
    import tempfile
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        tmp.write(b"data")
        tmp_name = tmp.name
    try:
        d = {
            "dataset_id": "3012010101",
            "target_name": "PSR J0030+0451",
            "instrument": "NICER",
            "observable_type": "nicer_surface_redshift_proxy",
            "local_path": tmp_name,
            "data_level": "raw",
            "validation_category": "standard",
            "limitations": ["none"]
        }
        target = {
            "mass_solar": 1.4,
            "radius_km": 13.0,
            "allowed_for_canonical_gate": True,
            "independent_parameter_sources": [{"parameter": "mass", "source_type": "independent_literature"}],
            "limitations": ["none"]
        }
        res = run_single_countertest(d, target, "nicer_surface_redshift_proxy")
        assert res["status"] in ["PASS_EXACT", "FAIL"]
    finally:
        import os
        if os.path.exists(tmp_name):
            os.remove(tmp_name)
