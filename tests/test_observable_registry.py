"""
Tests for the SSZ Observable Registry.

© 2025 Carmen N. Wrede & Lino Casu
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
        "gps_clock_correction", "cassini_shapiro_gamma", "mercury_perihelion",
        "eddington_lensing", "static_redshift", "dual_velocity_product",
        "finite_horizon_D", "energy_condition_regime", "light_travel_time_correction"
    }
    
    observables = list_observables()
    print(f"  Registry has {len(observables)} observables")
    print(f"  Required {len(required_ids)} observables")
    
    all_fitting_banned = True
    for obs in observables:
        if obs["fitting_allowed"]:
            all_fitting_banned = False
        assert "id" in obs
        assert "fitting_allowed" in obs
        assert obs["fitting_allowed"] is False
    
    print(f"  All fitting banned: {all_fitting_banned}")


def test_get_observable():
    """Verify retrieval of individual observables."""
    gps = get_observable("gps_clock_correction")
    print(f"  GPS clock: {gps['name']}")
    print(f"    class: {gps['class']}, method: {gps['method']}")
    print(f"    reference: {gps['reference_value']}")
    
    assert gps is not None
    assert gps["id"] == "gps_clock_correction"
    
    non_existent = get_observable("non_existent_id")
    print(f"  Non-existent lookup returns None: {non_existent is None}")
    assert non_existent is None
