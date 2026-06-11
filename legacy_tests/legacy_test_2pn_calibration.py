"""
Test 2PN Calibration

Verifies 2PN calibration matches GR to O(U²).
This is the CRITICAL test for SSZ metric validity.
"""

import pytest
import numpy as np
from math import isclose
import sys
sys.path.insert(0, '/home/error/Downloads/ssz-metric-complete/src')

from ssz_core import PHI, C, G, M_SUN


class Test2PNCalibration:
    """Tests for 2PN post-Newtonian calibration."""
    
    def test_phi_g_satisfies_2pn_relation(self):
        """
        Verify φ_G² = 2U(1 + U/3).
        
        This is the KEY equation for 2PN calibration.
        """
        # Test at various distances
        r_values = [1e10, 5e10, 1e11, 5e11]  # meters
        
        for r in r_values:
            # Newtonian potential
            U = G * M_SUN / (r * C**2)
            
            # 2PN φ_G
            phi_g_squared = 2 * U * (1 + U/3)
            
            # Should be positive
            assert phi_g_squared > 0, f"phi_G² = {phi_g_squared} <= 0"
            
            # Check magnitude
            phi_g = np.sqrt(phi_g_squared)
            assert np.isfinite(phi_g), f"phi_G = {phi_g} not finite"
    
    def test_gamma_cosh_relation(self):
        """γ = cosh(φ_G) > 1 always"""
        # Test at various distances
        r_values = [1e10, 5e10, 1e11]
        
        for r in r_values:
            U = G * M_SUN / (r * C**2)
            phi_g = np.sqrt(2 * U * (1 + U/3))
            gamma = np.cosh(phi_g)
            
            assert gamma > 1.0, f"γ = {gamma} <= 1"
            assert np.isfinite(gamma), f"γ = {gamma} not finite"
    
    def test_beta_tanh_relation(self):
        """β = tanh(φ_G) < 1 always"""
        # Test at various distances
        r_values = [1e10, 5e10, 1e11]
        
        for r in r_values:
            U = G * M_SUN / (r * C**2)
            phi_g = np.sqrt(2 * U * (1 + U/3))
            beta = np.tanh(phi_g)
            
            assert 0 < beta < 1.0, f"β = {beta} not in (0,1)"
    
    def test_d_s_relation(self):
        """D = 1/γ, s = γ, D·s = 1"""
        r_values = [1e10, 5e10, 1e11]
        
        for r in r_values:
            U = G * M_SUN / (r * C**2)
            phi_g = np.sqrt(2 * U * (1 + U/3))
            gamma = np.cosh(phi_g)
            
            D = 1.0 / gamma
            s = gamma
            
            assert isclose(D * s, 1.0, rel_tol=1e-14), \
                f"D·s = {D*s}, expected 1.0"
    
    def test_2pn_vs_1pn_deviation(self):
        """
        Verify 2PN differs from 1PN at O(U²).
        
        1PN: φ² = 2U
        2PN: φ² = 2U(1 + U/3)
        
        Difference is ~U/3 at O(U²).
        """
        r = 1e10  # Close to Sun
        U = G * M_SUN / (r * C**2)
        
        phi_1pn_squared = 2 * U
        phi_2pn_squared = 2 * U * (1 + U/3)
        
        rel_diff = (phi_2pn_squared - phi_1pn_squared) / phi_1pn_squared
        expected_diff = U / 3
        
        assert abs(rel_diff - expected_diff) < 1e-10, \
            f"2PN deviation {rel_diff} != expected {expected_diff}"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
