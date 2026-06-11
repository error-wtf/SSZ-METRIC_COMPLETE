"""
Tests for observable derivation contract.
"""
import pytest
from ssz_metric_pure.external_observable_derivation import (
    derive_nicer_observables,
    derive_alma_observables
)

def test_derivation_contract():
    entry = {"observable_type": "nicer_surface_redshift_proxy", "instrument": "NICER"}
    # Create fake file to test loading
    import tempfile
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        tmp.write(b"data")
        tmp_name = tmp.name
    try:
        derived = derive_nicer_observables(entry, tmp_name)
        assert derived["observable_type"] == "nicer_surface_redshift_proxy"
    finally:
        import os
        if os.path.exists(tmp_name):
            os.remove(tmp_name)
