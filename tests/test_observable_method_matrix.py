"""
Tests for the Prime Directive Method Matrix Routing.

Verifies that physical observables map to the mathematically correct and allowed
method routing paths as specified by the Matrix guidelines.

© 2025 Carmen Wrede & Lino Casu
Licensed under the Anti-Capitalist Software License v1.4
"""

import pytest
from ssz_metric_pure.observable_registry import get_observable, list_observables


@pytest.mark.parametrize("obs_id, expected_class, expected_method", [
    ("eddington_lensing", "NULL_LIGHT", "PPN_COMPLETION"),
    ("cassini_shapiro_gamma", "NULL_LIGHT", "PPN_COMPLETION"),
    ("light_travel_time_correction", "NULL_LIGHT", "PPN_COMPLETION"),
    ("static_redshift", "TIMELIKE_STATIC", "XI_DIRECT"),
    ("gps_clock_correction", "TIMELIKE_STATIC", "XI_DIRECT"),
    ("mercury_perihelion", "TIMELIKE_ORBIT", "PPN_ORBIT"),
    ("dual_velocity_product", "KINEMATIC_INVARIANT", "SSZ_KINEMATIC_IDENTITY"),
    ("finite_horizon_D", "STRONG_FIELD_DIAGNOSTIC", "XI_STRONG_FIELD_DIAGNOSTIC"),
    ("energy_condition_regime", "STRONG_FIELD_DIAGNOSTIC", "XI_STRONG_FIELD_DIAGNOSTIC")
])
def test_observable_method_matrix_routing(obs_id, expected_class, expected_method):
    """Verify that specific observables route to exactly the correct matrix method."""
    obs = get_observable(obs_id)
    assert obs is not None, f"Observable '{obs_id}' not found in registry!"
    assert obs["class"] == expected_class, f"Mismatch class for {obs_id}: {obs['class']} != {expected_class}"
    assert obs["method"] == expected_method, f"Mismatch method for {obs_id}: {obs['method']} != {expected_method}"


def test_entire_registry_routing_rules():
    """Verify that every single observable in the registry conforms toallowed routing classes and methods."""
    allowed_methods = {
        "PPN_COMPLETION",
        "XI_DIRECT",
        "PPN_ORBIT",
        "SSZ_KINEMATIC_IDENTITY",
        "XI_STRONG_FIELD_DIAGNOSTIC"
    }
    allowed_classes = {
        "NULL_LIGHT",
        "TIMELIKE_STATIC",
        "TIMELIKE_ORBIT",
        "KINEMATIC_INVARIANT",
        "STRONG_FIELD_DIAGNOSTIC"
    }
    
    for obs in list_observables():
        assert obs["class"] in allowed_classes, f"Observable {obs['id']} has invalid class {obs['class']}"
        assert obs["method"] in allowed_methods, f"Observable {obs['id']} has invalid method {obs['method']}"
