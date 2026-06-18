"""
Tests for the SSZ Planck and Fine-Structure Adjacent Scale Domain.

© 2025 Carmen N. Wrede & Lino Casu
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
    expected = 1.618033988749895
    print(f"  Phi constant: {phi:.15f}")
    print(f"  Expected: {expected:.15f}")
    print(f"  Error: {abs(phi - expected):.2e}")
    assert isclose(phi, expected, rel_tol=1e-12)


def test_alpha_reference():
    """Verify physical fine structure constant reference."""
    alpha = alpha_reference()
    inverse_alpha = 1.0 / alpha
    expected = 137.035999084
    print(f"  1/alpha = {inverse_alpha:.9f}")
    print(f"  Expected: {expected:.9f}")
    print(f"  Error: {abs(inverse_alpha - expected):.2e}")
    assert isclose(inverse_alpha, expected, rel_tol=1e-12)


def test_fine_structure_proxy():
    """Verify that fine structure proxy returns a finite, positive scale factor."""
    proxy = fine_structure_proxy()
    print(f"  Fine structure proxy: {proxy:.10f}")
    print(f"  Expected: 0 < proxy < 1")
    assert proxy > 0.0
    assert proxy < 1.0


def test_planck_scale_context_and_limitations():
    """Verify Planck scaling parameters and explicit limitations."""
    context = planck_scale_context()
    print(f"  Planck length: {context['planck_length']:.2e} m")
    print(f"  Planck mass: {context['planck_mass']:.2e} kg")
    print(f"  Planck time: {context['planck_time']:.2e} s")
    
    assert "planck_length" in context
    assert "planck_mass" in context
    assert "planck_time" in context
    assert "limitations" in context
    
    # Assert exact required disclaimer sentence is present
    expected_clause = "This domain encodes SSZ's structural lower-scale constants and fine-structure-adjacent relations. It does not by itself prove a complete theory of quantum gravity."
    print(f"  Limitations clause present: {context['limitations'] == expected_clause}")
    assert context["limitations"] == expected_clause
