"""
Tests for checking external anti-circularity verification constraints.

© 2026 Carmen N. Wrede & Lino Casu
Licensed under the Anti-Capitalist Software License v1.4
"""

import pytest
from ssz_metric_pure.external_countertests import check_external_anticircularity


def test_anticircularity():
    # Valid entry
    d = {
        "dataset_id": "test_1",
        "target_name": "PSR J0030+0451",
        "data_level": "raw",
        "validation_category": "standard",
        "limitations": ["none"]
    }
    t = {
        "target_name": "PSR J0030+0451",
        "independent_parameter_sources": [{"parameter": "mass", "source_type": "independent_literature"}],
        "limitations": ["none"]
    }
    
    ac = check_external_anticircularity(d, t, "nicer_surface_redshift_proxy")
    assert ac["anti_circular"] is True
    
    # Invalid missing data_level
    d_bad = d.copy()
    del d_bad["data_level"]
    ac_bad = check_external_anticircularity(d_bad, t, "nicer_surface_redshift_proxy")
    assert ac_bad["anti_circular"] is False
