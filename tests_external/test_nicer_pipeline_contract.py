"""
Contract and forward prediction tests for the NICER validation pipeline.

© 2026 Carmen N. Wrede & Lino Casu
Licensed under the Anti-Capitalist Software License v1.4
"""

import os
import pytest
from tempfile import TemporaryDirectory
from ssz_metric_pure.external_fetch_common import write_json
from ssz_metric_pure.nicer_validation import (
    load_nicer_manifest,
    validate_nicer_manifest_entry,
    derive_nicer_observable,
    predict_nicer_ssz,
    compare_nicer_prediction,
    run_nicer_validation
)


def test_nicer_pipeline_contract():
    """Verify that predictions, derivations, and comparisons follow the non-circular pipeline flow."""
    with TemporaryDirectory() as tmpdir:
        # Create a mock manifest
        manifest_p = os.path.join(tmpdir, "nicer.json")
        local_data_p = os.path.join(tmpdir, "3012010101.evt")
        with open(local_data_p, "w") as f:
            f.write("mock event data")
            
        manifest = {
            "schema_version": "1.0",
            "created_utc": "2026-06-11T12:00:00Z",
            "created_by": "scripts/fetch_nicer.py",
            "instrument": "NICER",
            "datasets": [
                {
                    "dataset_id": "3012010101",
                    "target_name": "PSR J0030+0451",
                    "obs_id_or_project_code": "3012010101",
                    "archive": "HEASARC",
                    "access_url": "https://heasarc.gsfc.nasa.gov/FTP/nicer/data/obs/30/3012010101/",
                    "local_path": local_data_p,
                    "validation_category": "raw_data",
                    "model_dependency": "none",
                    "observable_type": "redshift"
                }
            ]
        }
        write_json(manifest_p, manifest)
        
        # Test loading
        man = load_nicer_manifest(manifest_p)
        assert len(man["datasets"]) == 1
        
        entry = man["datasets"][0]
        assert validate_nicer_manifest_entry(entry) is True
        
        # Derive
        derived = derive_nicer_observable(entry)
        assert derived["observable_type"] == "redshift"
        assert "value" in derived
        
        # Predict
        pred = predict_nicer_ssz(entry)
        assert pred["observable_type"] == "redshift"
        assert pred["value"] > 0.0
        
        # Compare
        comp = compare_nicer_prediction(entry, pred, derived)
        assert comp["status"] in ["PASS", "WARN", "FAIL"]
        assert comp["anti_circularity"] == "PASS"
        
        # Test full runner
        reports = run_nicer_validation(manifest_p)
        assert len(reports) == 1
        assert reports[0]["status"] in ["PASS", "WARN", "FAIL"]
