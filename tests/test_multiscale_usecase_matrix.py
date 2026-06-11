"""
Structural Verification Test of the SSZ Multi-Scale Usecase Matrix.

© 2025 Carmen N. Wrede & Lino Casu
Licensed under the Anti-Capitalist Software License v1.4
"""

import os
import pytest
from pathlib import Path


def test_domain_docs_and_matrix_existence():
    """Verify that all scale domain docs and matrices exist in the repository."""
    repo_root = Path(__file__).resolve().parent.parent
    
    assert (repo_root / "docs/SSZ_USECASE_MATRIX.md").exists()
    assert (repo_root / "docs/SCALE_DOMAIN_PLANCK_FINE_STRUCTURE.md").exists()
    assert (repo_root / "docs/SCALE_DOMAIN_PHI_LATTICE.md").exists()
    assert (repo_root / "docs/SCALE_DOMAIN_PHASE_FREQUENCY.md").exists()
    assert (repo_root / "docs/SCALE_DOMAIN_STRONG_FIELD.md").exists()
    assert (repo_root / "docs/SCALE_DOMAIN_NEUTRON_STAR.md").exists()


def test_domain_modules_imports():
    """Verify that all seven scale domain modules import successfully and expose reports or metadata."""
    from ssz_metric_pure.fine_structure import planck_scale_context
    from ssz_metric_pure.phi_lattice import segment_distance
    from ssz_metric_pure.phase_frequency import local_c_invariance_check
    from ssz_metric_pure.clock_observables import time_dilation_D
    from ssz_metric_pure.ppn import ppn_gamma
    from ssz_metric_pure.strong_field import strong_field_regime_report
    from ssz_metric_pure.neutron_star import neutron_star_usecase_report
    
    # Simple sanity checks
    assert planck_scale_context()["planck_length"] > 0.0
    assert ppn_gamma() == 1.0


def test_domains_list_and_limitations():
    """Verify the scale domain registry listings and limitations statements."""
    from ssz_metric_pure.scale_domains import list_scale_domains
    domains = list_scale_domains()
    assert len(domains) == 7
    
    for dom in domains:
        assert "name" in dom
        assert "physical_scale" in dom
        assert "primary_quantities" in dom
        assert "limitations" in dom
        assert "validation_status" in dom
        
        # Verify validation statuses are honest, non-overclaim categories
        allowed_statuses = {
            "internal identity tested",
            "forward formula tested",
            "external reference formula tested",
            "external observational validation pending",
            "exploratory only"
        }
        assert dom["validation_status"] in allowed_statuses
