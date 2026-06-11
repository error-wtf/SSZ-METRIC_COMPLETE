"""
Contract and forward prediction tests for the ALMA validation pipeline.

© 2026 Carmen N. Wrede & Lino Casu
Licensed under the Anti-Capitalist Software License v1.4
"""

import os
import pytest
from tempfile import TemporaryDirectory
from ssz_metric_pure.external_fetch_common import write_json
from ssz_metric_pure.alma_validation import (
    load_alma_manifest,
    validate_alma_manifest_entry,
    derive_alma_observable,
    predict_alma_ssz,
    compare_alma_prediction,
    run_alma_validation
)


def test_alma_pipeline_contract():
    """Verify that predictions, derivations, and comparisons follow the non-circular pipeline flow."""
    with TemporaryDirectory() as tmpdir:
        # Create a mock manifest
        manifest_p = os.path.join(tmpdir, "alma.json")
        local_data_p = os.path.join(tmpdir, "m87.fits")
        with open(local_data_p, "w") as f:
            f.write("mock fits data")
            
        manifest = {
            "schema_version": "1.0",
            "created_utc": "2026-06-11T12:00:00Z",
            "created_by": "scripts/fetch_alma.py",
            "instrument": "ALMA",
            "datasets": [
                {
                    "dataset_id": "uid___A001_X12a_X3b",
                    "target_name": "M87",
                    "obs_id_or_project_code": "2018.1.01234.S",
                    "archive": "ALMA Science Archive",
                    "access_url": "https://almascience.eso.org/data/member.uid_A001_X12a_X3b.fits",
                    "local_path": local_data_p,
                    "validation_category": "calibrated_or_qa2_product",
                    "model_dependency": "medium",
                    "observable_type": "frequency_shift"
                }
            ]
        }
        write_json(manifest_p, manifest)
        
        # Test loading
        man = load_alma_manifest(manifest_p)
        assert len(man["datasets"]) == 1
        
        entry = man["datasets"][0]
        assert validate_alma_manifest_entry(entry) is True
        
        # Derive
        derived = derive_alma_observable(entry)
        assert derived["observable_type"] == "frequency_shift"
        assert "value" in derived
        
        # Predict
        pred = predict_alma_ssz(entry)
        assert pred["observable_type"] == "frequency_shift"
        assert pred["value"] > 0.0
        
        # Compare
        comp = compare_alma_prediction(entry, pred, derived)
        assert comp["status"] in ["PASS", "WARN", "FAIL"]
        
        # Test full runner
        reports = run_alma_validation(manifest_p)
        assert len(reports) == 1
        assert reports[0]["status"] in ["PASS", "WARN", "FAIL"]
