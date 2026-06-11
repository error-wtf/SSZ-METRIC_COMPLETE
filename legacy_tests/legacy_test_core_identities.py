"""
Test Core Identities of SSZ-Core.

Verifies:
- γ >= 1
- |β| < 1
- D * s == 1 (from 10 r_s to 1e6 r_s with tolerance < 1e-12)
- Ξ == γ - 1
- D == 1/γ
- s == γ

© 2025 Carmen Wrede & Lino Casu
Licensed under the Anti-Capitalist Software License v1.4
"""

import pytest
import numpy as np
from ssz_metric_pure import (
    phi_G_2pn, gamma_of_phi, beta_of_phi, D_of_gamma, s_of_gamma, xi_of_gamma,
    xi_field_2pn, D_of_xi, s_of_xi, gamma_of_xi, beta_of_xi, M_SUN, G, C
)

def test_core_identities():
    """Verify that fundamental algebraic and physical identities are strictly satisfied."""
    r_s = (2.0 * G * M_SUN) / (C ** 2)
    
    # Range from 10 r_s to 1e6 r_s
    r_vals = np.logspace(1, 6, 100) * r_s
    
    for r in r_vals:
        # Axiomatic path (primary field first)
        xi_axiom = xi_field_2pn(r, M_SUN)
        D_axiom = D_of_xi(xi_axiom)
        s_axiom = s_of_xi(xi_axiom)
        gam_axiom = gamma_of_xi(xi_axiom)
        bet_axiom = beta_of_xi(xi_axiom)
        
        # Legacy/Compatibility path
        phi = phi_G_2pn(r, M_SUN)
        gam = gamma_of_phi(phi)
        bet = beta_of_phi(phi)
        D = D_of_gamma(gam)
        s = s_of_gamma(gam)
        xi = xi_of_gamma(gam)
        
        # Verify 100% equivalence between primary-field derived variables and legacy forms
        assert abs(xi_axiom - xi) < 1e-14
        assert abs(D_axiom - D) < 1e-14
        assert abs(s_axiom - s) < 1e-14
        assert abs(gam_axiom - gam) < 1e-14
        assert abs(bet_axiom - bet) < 1e-12
        
        # 1. gamma >= 1
        assert gam_axiom >= 1.0
        
        # 2. abs(beta) < 1
        assert abs(bet_axiom) < 1.0
        
        # 3. D * s == 1 with high tolerance
        assert abs(D_axiom * s_axiom - 1.0) < 1e-12
        
        # 4. xi = gamma - 1
        assert abs(xi_axiom - (gam_axiom - 1.0)) < 1e-15
        
        # 5. D = 1/gamma
        assert abs(D - 1.0 / gam) < 1e-15
        
        # 6. s = gamma
        assert abs(s - gam) < 1e-15
