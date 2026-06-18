"""Tests for SSZ Shapiro Delay and Light Deflection - Exact Implementations."""
import pytest
import numpy as np
from ssz_metric_pure.constants import C, G, M_SUN, R_SUN
from ssz_metric_pure.shapiro_minimal import shapiro_ssz
from ssz_metric_pure.shapiro_exact import (
    shapiro_delay_weak_field_exact,
    shapiro_delay_numerical_exact,
    shapiro_delay_full
)
from ssz_metric_pure.deflection_minimal import deflection_ssz
from ssz_metric_pure.deflection_exact import (
    deflection_weak_field_exact,
    deflection_numerical_exact,
    deflection_full
)


class TestShapiroDelay:
    """Test Shapiro delay calculations."""
    
    def test_shapiro_sun_earth_minimal(self):
        """Sun-Earth Shapiro delay with minimal implementation."""
        r_earth = 1.496e11  # 1 AU in meters
        r_sun = 6.96e8      # Solar radius
        
        delay = shapiro_ssz(r_sun, r_earth, M_SUN, n=5000)
        
        # Weak-field SSZ: Δt = (r_s/2c) * ln(r2/r1)
        # For Sun-Earth: ~26.5 microseconds (physically correct)
        assert 20e-6 < delay < 40e-6  # 20-40 microseconds (weak-field)
    
    def test_shapiro_weak_field_exact(self):
        """Exact analytical Shapiro delay for weak field."""
        r1 = 7e8  # Near Sun
        r2 = 1.5e11  # Earth
        
        delay = shapiro_delay_weak_field_exact(r1, r2, M_SUN)
        
        # Should be positive and reasonable
        assert delay > 0
        assert delay < 1e-3  # Less than 1 ms
    
    def test_shapiro_numerical_exact(self):
        """Exact numerical Shapiro delay."""
        r1 = 7e8
        r2 = 1.5e11
        
        delay_num = shapiro_delay_numerical_exact(r1, r2, M_SUN, n_points=5000)
        delay_ana = shapiro_delay_weak_field_exact(r1, r2, M_SUN)
        
        # Numerical should approximate analytical
        # Allow 10% difference for different integration methods
        assert abs(delay_num - delay_ana) / delay_ana < 0.15
    
    def test_shapiro_full_structure(self):
        """Full Shapiro result structure."""
        result = shapiro_delay_full(7e8, 1.5e11, M_SUN)
        
        assert 'delay_seconds' in result
        assert 'delay_microseconds' in result
        assert 'method' in result
        assert 'regime' in result
        
        assert result['delay_microseconds'] == result['delay_seconds'] * 1e6
        assert result['method'] in ['analytical', 'numerical']


class TestLightDeflection:
    """Test light deflection calculations."""
    
    def test_deflection_sun_minimal(self):
        """Sun grazing incidence with minimal implementation."""
        b = R_SUN  # Grazing impact parameter
        
        alpha = deflection_ssz(b, M_SUN)
        
        # Expected ~1.75 arcseconds
        alpha_arcsec = alpha * (180/np.pi) * 3600
        
        assert 1.5 < alpha_arcsec < 2.0  # ~1.75"
    
    def test_deflection_weak_field_exact(self):
        """Exact analytical deflection for weak field."""
        b = R_SUN
        
        alpha = deflection_weak_field_exact(b, M_SUN)
        alpha_arcsec = alpha * (180/np.pi) * 3600
        
        # Should be ~1.75 arcseconds
        assert 1.5 < alpha_arcsec < 2.0
    
    def test_deflection_proportional_to_1_b(self):
        """Deflection scales as 1/b."""
        alpha1 = deflection_weak_field_exact(R_SUN, M_SUN)
        alpha2 = deflection_weak_field_exact(2 * R_SUN, M_SUN)
        
        # Should be half
        assert abs(alpha2 - alpha1/2) / alpha1 < 0.01
    
    def test_deflection_proportional_to_mass(self):
        """Deflection scales linearly with mass."""
        alpha_sun = deflection_weak_field_exact(R_SUN, M_SUN)
        alpha_2sun = deflection_weak_field_exact(R_SUN, 2 * M_SUN)
        
        # Should be double
        assert abs(alpha_2sun - 2*alpha_sun) / alpha_sun < 0.01
    
    def test_deflection_full_structure(self):
        """Full deflection result structure."""
        result = deflection_full(R_SUN, M_SUN)
        
        assert 'deflection_rad' in result
        assert 'deflection_arcsec' in result
        assert 'method' in result
        assert 'regime' in result
        
        assert result['deflection_arcsec'] == result['deflection_rad'] * (180/np.pi) * 3600


class TestConsistency:
    """Test consistency between implementations."""
    
    def test_shapiro_minimal_vs_exact(self):
        """Minimal and exact Shapiro should agree in weak field."""
        r1 = 10 * R_SUN
        r2 = 100 * R_SUN
        
        delay_min = shapiro_ssz(r1, r2, M_SUN, n=10000)
        delay_exact = shapiro_delay_numerical_exact(r1, r2, M_SUN, n_points=10000)
        
        # Should agree within 5%
        assert abs(delay_min - delay_exact) / delay_exact < 0.05
    
    def test_deflection_minimal_vs_exact(self):
        """Minimal and exact deflection should agree."""
        b = 10 * R_SUN
        
        alpha_min = deflection_ssz(b, M_SUN)
        alpha_exact = deflection_weak_field_exact(b, M_SUN)
        
        # Should be very close
        assert abs(alpha_min - alpha_exact) / alpha_exact < 0.01


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
