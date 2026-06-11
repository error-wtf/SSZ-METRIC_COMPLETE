"""
Tests for checking external validation report generation.

© 2026 Carmen N. Wrede & Lino Casu
Licensed under the Anti-Capitalist Software License v1.4
"""

import os
import pytest
from tempfile import TemporaryDirectory
from ssz_metric_pure.external_fetch_common import write_json
from ssz_metric_pure.external_validation_report import generate_external_validation_report


def test_validation_report_generation():
    """Verify that generate_external_validation_report compiles sections correctly."""
    with TemporaryDirectory() as tmpdir:
        nicer_man = os.path.join(tmpdir, "nicer.json")
        alma_man = os.path.join(tmpdir, "alma.json")
        
        # Write mock manifests
        manifest_nicer = {
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
                    "local_path": "non_existent.evt",
                    "validation_category": "raw_data",
                    "model_dependency": "none",
                    "observable_type": "redshift"
                }
            ]
        }
        write_json(nicer_man, manifest_nicer)
        write_json(alma_man, manifest_nicer)  # use same mock data structure
        
        rep_p = os.path.join(tmpdir, "REPORT.md")
        generate_external_validation_report(nicer_man, alma_man, rep_p)
        assert os.path.exists(rep_p)
        
        with open(rep_p, "r", encoding="utf-8") as f:
            content = f.read()
            
        required_headers = [
            "# External NICER / ALMA Data Validation Report",
            "## 1. Purpose",
            "## 2. Source of Truth",
            "## 3. External Data Protocol",
            "## 4. NICER Gate Results",
            "## 5. ALMA Gate Results",
            "## 6. Forward Chain Verification",
            "## 7. Anti-Circularity Checks",
            "## 8. Data Dependency Classification",
            "## 9. Model-Dependency Classification",
            "## 10. PASS/WARN/FAIL/SKIP Summary",
            "## 11. What This Validates",
            "## 12. What This Does Not Validate",
            "## 13. Next Required Real-Data Steps"
        ]
        
        for h in required_headers:
            assert h in content, f"Required markdown section heading '{h}' is missing from report."
            
        # Assert exact disclaimer sentence is present
        disclaimer = "External NICER/ALMA gates compare SSZ forward predictions against independently derived observables where possible. High model-dependency or same-dataset parameter inference is explicitly marked as exploratory and cannot be counted as hard external validation."
        assert disclaimer in content, "Required model dependency disclaimer sentence is missing from report."
