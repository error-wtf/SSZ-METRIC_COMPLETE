"""
Tests for checking external data manifest schema conformity.

© 2026 Carmen N. Wrede & Lino Casu
Licensed under the Anti-Capitalist Software License v1.4
"""

import os
from ssz_metric_pure.external_fetch_common import read_json
from ssz_metric_pure.external_data import validate_manifest_schema


def test_manifest_schema_conformity():
    """Verify that both standard and example manifests comply with the schema."""
    nicer_ex = "external_validation/manifests/nicer/example_nicer_manifest.json"
    alma_ex = "external_validation/manifests/alma/example_alma_manifest.json"
    
    assert os.path.exists(nicer_ex)
    assert os.path.exists(alma_ex)
    
    nicer_data = read_json(nicer_ex)
    alma_data = read_json(alma_ex)
    
    assert validate_manifest_schema(nicer_data) is True
    assert validate_manifest_schema(alma_data) is True
