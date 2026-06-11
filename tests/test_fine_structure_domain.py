"""
Tests for the SSZ Planck and Fine-Structure Adjacent Scale Domain.

© 2025 Carmen Wrede & Lino Casu
Licensed under the Anti-Capitalist Software License v1.4
"""

import pytest
from math import isclose
from ssz_metric_pure.fine_structure import (
    phi_constant,
    alpha_reference,
    fine_structure_proxy,
    planck_scale_context
)


def test_phi_constant():
    """Verify phi constant value matches Golden Ratio."""
    phi = phi_constant()
    assert isclose(phi, 1.618033988749895, rel_tol=1e-12)


def test_alpha_reference():
    """Verify physical fine structure constant reference."""
    alpha = alpha_reference()
    assert isclose(1.0 / alpha, 137.035999084, rel_tol=1e-12)


def test_fine_structure_proxy():
    """Verify that fine structure proxy returns a finite, positive scale factor."""
    proxy = fine_structure_proxy()
    assert proxy > 0.0
    assert proxy < 1.0


def test_planck_scale_context_and_limitations():
    """Verify Planck scaling parameters and explicit limitations."""
    context = planck_scale_context()
    assert "planck_length" in context
    assert "planck_mass" in context
    assert "planck_time" in context
    assert "limitations" in context
    
    # Assert exact required disclaimer sentence is present
    expected_clause = "This domain encodes SSZ's structural lower-scale constants and fine-structure-adjacent relations. It does not by itself prove a complete theory of quantum gravity."
    assert context["limitations"] == expected_clause
