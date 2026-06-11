"""
Test of standard package imports.

© 2025 Carmen N. Wrede & Lino Casu
Licensed under the Anti-Capitalist Software License v1.4
"""

import pytest

def test_package_import():
    """Verify that the ssz_metric_pure package imports successfully and exposes canonical API."""
    import ssz_metric_pure
    assert ssz_metric_pure.__version__ == "1.1.0-canonical-pure"
    assert "xi_canonical" in dir(ssz_metric_pure)
    assert "D_from_xi" in dir(ssz_metric_pure)
    assert "s_from_xi" in dir(ssz_metric_pure)
