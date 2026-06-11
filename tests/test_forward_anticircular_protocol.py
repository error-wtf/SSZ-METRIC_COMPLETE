"""
Tests for the SSZ Forward and Anti-Circular Validation Protocol.

© 2025 Carmen Wrede & Lino Casu
Licensed under the Anti-Capitalist Software License v1.4
"""

import pytest
from ssz_metric_pure.forward_protocol import (
    run_all_protocols,
    validate_no_fitting_used,
    validate_inputs_fixed_before_comparison,
    validate_formula_source_declared,
    validate_observable_method_assignment,
    validate_reference_not_used_in_prediction,
    validate_claim_scope
)


def test_no_fitting_validation_protocol():
    """Verify that the fitting ban scan executes and passes successfully."""
    res = validate_no_fitting_used()
    assert res["status"] == "PASS"
    assert "reason" in res


def test_inputs_fixed_before_comparison():
    """Verify that inputs are statically declared beforehand."""
    res = validate_inputs_fixed_before_comparison()
    assert res["status"] == "PASS"


def test_formula_source_declared():
    """Verify that all observables declare an explicit documentation source."""
    res = validate_formula_source_declared()
    assert res["status"] == "PASS"


def test_observable_method_assignment():
    """Verify that only valid Prime Directive classes and methods are assigned."""
    res = validate_observable_method_assignment()
    assert res["status"] == "PASS"


def test_reference_not_used_in_prediction():
    """Verify that prediction functions have zero access to reference datasets."""
    res = validate_reference_not_used_in_prediction()
    assert res["status"] == "PASS"


def test_claim_scope():
    """Verify that there are no marketing overclaims in prediction docstrings."""
    res = validate_claim_scope()
    assert res["status"] == "PASS"


def test_all_protocols():
    """Verify that running all protocols returns a consistent passing outcome."""
    protocols = run_all_protocols()
    for prot in protocols:
        assert isinstance(prot, dict)
        assert prot["status"] == "PASS"
        assert "gate" in prot
        assert "reason" in prot
        assert "files_checked" in prot
