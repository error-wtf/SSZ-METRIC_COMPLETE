"""
Tests for Forward and Anti-Circularity of Multi-Scale Domain Records.

© 2025 Carmen Wrede & Lino Casu
Licensed under the Anti-Capitalist Software License v1.4
"""

import pytest
from ssz_metric_pure.scale_domains import list_scale_domains


def test_multiscale_anti_circularity_registry_records():
    """Verify that all scale domain records are configured for anti-circular forward propagation."""
    for dom in list_scale_domains():
        assert "name" in dom
        assert "primary_quantities" in dom
        assert "implemented_functions" in dom
        assert "limitations" in dom
        assert "validation_status" in dom
        
        # Verify limitations are explicitly stated for each domain
        assert len(dom["limitations"]) > 0
        
        # Verify validation statuses map to anti-circularity guidelines
        assert dom["validation_status"] in (
            "internal identity tested",
            "forward formula tested",
            "external reference formula tested",
            "external observational validation pending",
            "exploratory only"
        )
