"""
Tests for prediction binding contract.
"""
import pytest
from ssz_metric_pure.external_prediction_bindings import (
    predict_for_external_observable
)

def test_prediction_bindings():
    params = {"mass_solar": 1.4, "radius_km": 13.0}
    pred = predict_for_external_observable("nicer_surface_redshift_proxy", params, {})
    assert pred["observable_type"] == "nicer_surface_redshift_proxy"
    assert pred["value"] > 0.0
