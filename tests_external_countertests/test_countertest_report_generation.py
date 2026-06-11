"""
Tests for checking countertest report generation.

© 2026 Carmen N. Wrede & Lino Casu
Licensed under the Anti-Capitalist Software License v1.4
"""

import os
from tempfile import TemporaryDirectory
from ssz_metric_pure.external_countertest_report import generate_external_countertest_report


def test_countertest_report_generation():
    with TemporaryDirectory() as tmpdir:
        rep_p = os.path.join(tmpdir, "REPORT.md")
        json_p = os.path.join(tmpdir, "results.json")
        
        results = [
            {
                "dataset_id": "3012010101",
                "target_name": "PSR J0030+0451",
                "instrument": "NICER",
                "status": "PASS_EXACT",
                "observable_type": "nicer_surface_redshift_proxy",
                "prediction": {"value": 0.170669},
                "derived_observable": {"value": 0.170669},
                "absolute_residual": 0.0,
                "relative_residual": 0.0,
                "comparison_mode": "EXACT_DERIVED_OBSERVABLE_MODE"
            }
        ]
        
        generate_external_countertest_report(results, rep_p, json_p)
        assert os.path.exists(rep_p)
        assert os.path.exists(json_p)
        
        with open(rep_p, "r", encoding="utf-8") as f:
            content = f.read()
            
        assert "## 10. Exact Benchmark Replay" in content
        assert "## 11. Negative Controls" in content
        assert "PASS_EXACT" in content
