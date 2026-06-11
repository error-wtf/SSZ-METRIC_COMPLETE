"""
Tests for the SSZ Observable Registry.

© 2025 Carmen Wrede & Lino Casu
Licensed under the Anti-Capitalist Software License v1.4
"""

import os
from ssz_metric_pure.observable_registry import (
    OBSERVABLE_REGISTRY,
    get_observable,
    list_observables
)


def test_registry_entries_completeness():
    """Verify that all required observables exist in the registry with valid metadata fields."""
    required_ids = {
        "gps_clock_correction",
        "cassini_shapiro_gamma",
        "mercury_perihelion",
        "eddington_lensing",
        "static_redshift",
        "dual_velocity_product",
        "finite_horizon_D",
        "energy_condition_regime",
        "light_travel_time_correction"
    }
    
    observables = list_observables()
    assert len(observables) >= len(required_ids)
    
    for obs in observables:
        assert "id" in obs
        assert "name" in obs
        assert "class" in obs
        assert "method" in obs
        assert "formula_source" in obs
        assert "implementation_function" in obs
        assert "input_parameters" in obs
        assert "reference_value" in obs
        assert "reference_uncertainty" in obs
        assert "source_note" in obs
        assert "test_scope" in obs
        assert "validation_type" in obs
        assert "fitting_allowed" in obs
        assert "limitations" in obs
        
        # Verify fitting is absolutely banned for all entries
        assert obs["fitting_allowed"] is False


def test_get_observable():
    """Verify retrieval of individual observables."""
    gps = get_observable("gps_clock_correction")
    assert gps is not None
    assert gps["id"] == "gps_clock_correction"
    
    non_existent = get_observable("non_existent_id")
    assert non_existent is None
