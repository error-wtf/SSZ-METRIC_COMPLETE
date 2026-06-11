"""
Test ssz_metric_pure package imports.

© 2025 Carmen Wrede & Lino Casu
Licensed under the Anti-Capitalist Software License v1.4
"""

def test_package_imports():
    """Verify that the package is correctly installed and all core exports are accessible."""
    import ssz_metric_pure
    from ssz_metric_pure import (
        PHI, C, G, M_SUN, R_SUN,
        U_of_r, phi_G_1pn, phi_G_2pn, gamma_of_phi, beta_of_phi, D_of_gamma, s_of_gamma, xi_of_gamma,
        PhiSpiralSSZMetric, SpiralMetricComponents, metric_diagonal, inverse_metric_diagonal,
        det_metric_diagonal, metric_flow_form,
        numerical_derivative_metric, christoffel_symbols, riemann_tensor,
        ricci_tensor, ricci_scalar, einstein_tensor,
        SSZObservableSuite, ObservableType
    )
    assert PHI > 1.618
    assert C == 299792458.0
