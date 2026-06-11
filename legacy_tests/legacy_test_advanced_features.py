"""
Test Advanced Features of the SSZ Metric

Tests for:
- Rotating Kerr-SSZ Metric
- Curvature and Tensor Geometry Engine (Numerical and Symbolic)
- Unified Observables Suite (Postulate 5 assignments)

© 2025 Carmen Wrede & Lino Casu
Licensed under the Anti-Capitalist Software License v1.4
"""

import pytest
import numpy as np
from math import isclose, pi
import sys
sys.path.insert(0, '/home/error/Downloads/ssz-metric-complete/src')

from ssz_core import (
    KerrSSZMetric,
    christoffel_numerical,
    riemann_numerical,
    ricci_numerical,
    einstein_numerical,
    symbolic_curvature_diagonal,
    SSZObservableSuite,
    ObservableType,
    PhiSpiralSSZMetric,
    SpiralMetricComponents,
    PHI, C, G, M_SUN, R_SUN
)


class TestRotatingKerrSSZ:
    """Tests for the rotating Kerr-SSZ metric."""
    
    def test_kerr_initialization(self):
        """Test proper initialization and bounds checks."""
        # Standard solar mass rotating SSZ black hole
        kerr = KerrSSZMetric(mass=M_SUN, spin_star=0.5)
        assert kerr.mass == M_SUN
        assert kerr.spin_star == 0.5
        assert kerr.r_s > 0
        
        # Test extremal spin limit checks (prevent J c / G M² >= 1.0)
        with pytest.raises(ValueError):
            KerrSSZMetric(mass=M_SUN, spin_star=1.0)
            
        with pytest.raises(ValueError):
            KerrSSZMetric(mass=-100, spin_star=0.5)

    def test_kerr_horizons_and_ergosphere(self):
        """Test calculation of event horizons and ergosphere boundaries."""
        # Solar mass with a* = 0.5 J c / (G M²)
        kerr = KerrSSZMetric(mass=M_SUN, spin_star=0.5)
        
        r_plus, r_minus = kerr.horizons()
        assert r_plus > r_minus
        assert r_plus > 0
        assert r_minus > 0
        
        # Ergosphere boundary at equator (theta = pi / 2) vs pole (theta = 0)
        r_ergo_equator = kerr.ergosphere(pi / 2.0)
        r_ergo_pole = kerr.ergosphere(0.0)
        
        assert r_ergo_equator > r_ergo_pole
        # At pole, ergosphere should coincide with outer horizon
        assert isclose(r_ergo_pole, r_plus, rel_tol=1e-12)

    def test_kerr_metric_components(self):
        """Test individual metric components for correct signs and limits."""
        kerr = KerrSSZMetric(mass=M_SUN, spin_star=0.5)
        
        # Large radius: should approach asymptotically flat limit
        r_far = 100 * kerr.r_s
        theta = pi / 4.0
        comps = kerr.metric_tensor(r_far, theta)
        
        # g_tt should be close to -1 (in C-scaled units)
        assert comps.g_tt < 0
        assert comps.g_rr > 0
        assert comps.g_thth > 0
        assert comps.g_phph > 0
        # Frame dragging g_tphi should decay rapidly with distance
        assert abs(comps.g_tph) < 100.0 * C


class TestCurvatureTensorEngine:
    """Tests for the numerical and symbolic curvature tensor calculations."""
    
    def test_christoffel_numerical(self):
        """Verify Christoffel symbols Γ^μ_νρ numerical calculations."""
        # Simple test: Schwarzschild-like static metric
        # Let's define a metric function for a simple static potential
        r_s = 2953.0
        
        def static_ssz_metric_func(t, r, theta, phi):
            # A_blended approximation
            N = 1.0 / (1.0 + r_s / (2 * max(r, 1e-12)))
            A = N**2
            g = np.zeros((4, 4))
            g[0, 0] = -A * C**2
            g[1, 1] = 1.0 / max(A, 1e-12)
            g[2, 2] = r**2
            g[3, 3] = r**2 * np.sin(theta)**2
            return g
            
        coords = (0.0, 10.0 * r_s, pi / 2.0, 0.0)
        Gamma = christoffel_numerical(static_ssz_metric_func, coords)
        
        # Test shape is 4x4x4
        assert Gamma.shape == (4, 4, 4)
        # Verify symmetry of lower indices Γ^μ_νρ = Γ^μ_ρν
        for mu in range(4):
            for nu in range(4):
                for rho in range(4):
                    assert isclose(Gamma[mu, nu, rho], Gamma[mu, rho, nu], abs_tol=1e-5)

    def test_symbolic_curvature(self):
        """Test symbolic curvature matrix generations."""
        import sympy as sp
        t, r, theta, phi = sp.symbols('t r theta phi', real=True)
        c = sp.symbols('c', positive=True)
        
        # Define a simple toy diagonal metric components
        g_tt = -c**2 * (1 - 1/r)
        g_rr = 1 / (1 - 1/r)
        g_thth = r**2
        g_phph = r**2 * sp.sin(theta)**2
        
        res = symbolic_curvature_diagonal(g_tt, g_rr, g_thth, g_phph, (t, r, theta, phi))
        
        assert "metric" in res
        assert "christoffel" in res
        assert "ricci_tensor" in res
        assert "ricci_scalar" in res
        assert "einstein_tensor" in res


class TestUnifiedObservables:
    """Tests for the unified observables suite enforcing Postulate 5."""
    
    def test_observable_redshift_and_dilation(self):
        """Verify redshift and time dilation use direct Xi-based timelike calculations."""
        suite = SSZObservableSuite(mass=M_SUN)
        
        # Redshift between 2 solar radii and 10 solar radii
        z = suite.evaluate_redshift(2.0 * R_SUN, 10.0 * R_SUN)
        assert z > 0  # Emitted deep, observed far -> redshift positive
        
        # Time dilation should be less than 1.0 (proper time runs slower relative to coordinate time)
        dtau = suite.evaluate_time_dilation(2.0 * R_SUN)
        assert 0.0 < dtau < 1.0

    def test_null_shapiro_delay(self):
        """Verify null Shapiro delay matches PPN assignments."""
        suite = SSZObservableSuite(mass=M_SUN)
        
        # Standard Sun-Earth shapiro round trip
        r_start = 1.5e11  # Earth distance (m)
        r_end = 1.5e11
        impact_param = R_SUN  # Grazing Sun
        
        delay = suite.evaluate_shapiro_delay(r_start, r_end, impact_param)
        
        # Should be around 110-150 microseconds for one-way solar grazing
        assert 100e-6 < delay < 200e-6

    def test_null_lensing(self):
        """Verify light deflection lensing matches PPN predictions."""
        suite = SSZObservableSuite(mass=M_SUN)
        
        # Solar grazing angle
        alpha = suite.evaluate_light_deflection(R_SUN)
        
        # Should be approximately 1.75 arcseconds (8.48e-6 radians)
        alpha_arcsec = alpha * (180.0 / pi) * 3600.0
        assert isclose(alpha_arcsec, 1.75, rel_tol=0.05)

    def test_timelike_orbit_precession(self):
        """Verify Mercury-like perihelion precession matches orbit formula."""
        suite = SSZObservableSuite(mass=M_SUN)
        
        # Mercury orbital parameters
        a_mercury = 5.7909e10  # semi-major axis (m)
        e_mercury = 0.20563    # eccentricity
        
        dphi_rad = suite.evaluate_perihelion_precession(a_mercury, e_mercury)
        
        # Convert to arcseconds per century (Mercury completes ~415 orbits per century)
        dphi_arcsec_century = dphi_rad * (180.0 / pi) * 3600.0 * 415.0
        
        # Should be close to the classical 43 arcseconds per century
        assert isclose(dphi_arcsec_century, 43.0, rel_tol=0.05)


class TestPurePhiSpiralSSZ:
    """Tests for the pure φ-Spiral SSZ metric."""
    
    def test_spiral_initialization(self):
        """Test spiral metric initialization and default profiles."""
        metric = PhiSpiralSSZMetric(mass=M_SUN, k=1.0)
        assert metric.mass == M_SUN
        assert metric.k == 1.0
        assert metric.r_s > 0
        
        # Test custom profile
        custom_metric = PhiSpiralSSZMetric(mass=M_SUN, phi_G_profile=lambda r: 2.0)
        assert custom_metric.phi_G(10.0) == 2.0
        
        with pytest.raises(ValueError):
            PhiSpiralSSZMetric(mass=-10.0)
            
    def test_spiral_fields(self):
        """Test calculation of beta, gamma, velocity and layer numbers."""
        metric = PhiSpiralSSZMetric(mass=M_SUN, k=1.0)
        
        # At r = 0, flat spacetime rotation = 0
        assert metric.phi_G(0.0) == 0.0
        assert metric.beta(0.0) == 0.0
        assert metric.gamma(0.0) == 1.0
        assert metric.time_dilation(0.0) == 1.0
        assert metric.subspace_layer(0.0) == 0
        
        # At large r, check values are bounded and physically consistent
        r_test = 5.0 * metric.r_s
        assert metric.phi_G(r_test) > 0.0
        assert 0.0 < metric.beta(r_test) < 1.0
        assert metric.gamma(r_test) > 1.0
        assert 0.0 < metric.time_dilation(r_test) < 1.0
        
    def test_spiral_metric_components(self):
        """Test pure spiral metric components and diagonal forms."""
        metric = PhiSpiralSSZMetric(mass=M_SUN, k=1.0)
        r = 3.0 * metric.r_s
        
        g = metric.metric_tensor(r)
        
        # Check shape and symmetry of off-diagonal term g_tr
        assert g.shape == (4, 4)
        assert g[0, 1] == g[1, 0] == metric.g_tr(r)
        
        # g_tt must be negative, g_rr positive
        assert g[0, 0] < 0
        assert g[1, 1] == 1.0  # g_rr = 1
        
        # Check diagonal form coefficients
        g_TT, g_rr_diag = metric.diagonal_form_coefficients(r)
        assert g_TT < 0
        assert g_rr_diag > 1.0  # γ² > 1

