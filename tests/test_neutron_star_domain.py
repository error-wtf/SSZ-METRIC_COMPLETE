"""
Tests for the SSZ Neutron Star Domain.

© 2025 Carmen N. Wrede & Lino Casu
Licensed under the Anti-Capitalist Software License v1.4
"""

import pytest
from math import isclose
from ssz_metric_pure.neutron_star import (
    neutron_star_compactness,
    neutron_star_regime,
    neutron_star_redshift_prediction,
    neutron_star_surface_D,
    neutron_star_usecase_report
)


def test_neutron_star_surface_physics():
    """Verify that compactness, surface temporal dilation, and redshifts are generated analytically."""
    M = 1.4 * 1.989e30  # 1.4 solar masses
    R = 12000.0         # 12 km radius
    
    comp = neutron_star_compactness(M, R)
    z = neutron_star_redshift_prediction(M, R)
    D = neutron_star_surface_D(M, R)
    
    print(f"  Neutron star: M = 1.4 M_sun, R = 12 km")
    print(f"  Compactness: {comp:.6f} (expected: 0 < comp < 1)")
    print(f"  Surface redshift z: {z:.6f}")
    print(f"  Surface D: {D:.6f} (expected: 1/(1+z) = {1.0/(1.0+z):.6f})")
    
    assert comp > 0.0
    assert comp < 1.0
    assert z > 0.0
    assert D > 0.0
    assert D < 1.0
    assert isclose(D, 1.0 / (1.0 + z), rel_tol=1e-12)


def test_neutron_star_report_and_limitations():
    """Verify neutron star report structures and explicit limitations."""
    M = 1.4 * 1.989e30
    R = 12000.0
    rep = neutron_star_usecase_report(M, R)
    
    print(f"  Neutron star report:")
    print(f"    Mass: {rep['mass_kg']:.3e} kg")
    print(f"    Radius: {rep['radius_m']:.1f} m")
    print(f"    Surface regime: {rep['surface_regime']}")
    print(f"    Fittings allowed: {rep['fittings_allowed']}")
    
    assert "mass_kg" in rep
    assert "radius_m" in rep
    assert "surface_regime" in rep
    assert "limitations" in rep
    assert rep["fittings_allowed"] is False
    
    # Verify exact caveats are documented
    expected_limitations = [
        "no full nuclear equation of state model",
        "no full rotating neutron-star model",
        "no full binary merger simulation",
        "no claim of complete observational proof",
        "this is a metric/regime/observable framework"
    ]
    for limit in expected_limitations:
        assert limit in rep["limitations"]
