"""
Tests verifying parameter manifest parsing and structure correctness.

© 2026 Carmen N. Wrede & Lino Casu
Licensed under the Anti-Capitalist Software License v1.4
"""

import os
import pytest
from ssz_metric_pure.external_parameter_manifest import (
    load_parameter_manifest,
    validate_parameter_manifest_schema,
    get_target_parameters
)


def test_parameter_manifest():
    path = "external_validation/countertests/parameter_manifest.json"
    assert os.path.exists(path)
    
    data = load_parameter_manifest(path)
    assert validate_parameter_manifest_schema(data) is True
    
    target = get_target_parameters(data, "PSR J0030+0451")
    assert target is not None
    assert target["target_id"] == "PSR_J0030_0451"
    
    non_existent = get_target_parameters(data, "Non Existent")
    assert non_existent is None
