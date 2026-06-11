"""
SSZ Core - Segmented Spacetime Z-Metric Core Module

This package implements the pure SSZ (Segmented Spacetime Z-Metric) formalism,
combining the best components from ssz-full-metric and ssz-metric-final.

© 2025 Carmen Wrede & Lino Casu
Licensed under the Anti-Capitalist Software License v1.4
"""

__version__ = "1.1.0-canonical"
__author__ = "Carmen Wrede & Lino Casu"

from .segment_density import (
    Xi,
    D_SSZ,
    D_GR,
    find_intersection,
)

from .blend_zone import (
    Xi_blend,
    Xi_complete,
    dXi_blend_dr,
    Xi_strong_raw,
    Xi_weak_raw,
    dXi_strong_raw,
    dXi_weak_raw,
)

from .metric import (
    A_Xi,
    A_phi_series,
    A_blended,
    A_safe,
    delta_M,
    corrected_r_s,
    metric_tensor,
)

from .constants import (
    PHI,
    C,
    G,
    M_SUN,
    R_SUN,
    X_BLEND_MIN,
    X_BLEND_MAX,
)

from .metric_kerr import (
    KerrSSZMetric,
    KerrMetricComponents,
    segment_density_N,
)

from .curvature import (
    christoffel_numerical,
    riemann_numerical,
    ricci_numerical,
    einstein_numerical,
    symbolic_curvature_diagonal,
)

from .observables import (
    ObservableType,
    SSZObservableSuite,
)

from .phi_spiral import (
    phi_g_squared,
    phi_g,
    gamma_factor,
    beta_factor,
    dtau_dt,
    PhiSpiralSSZMetric,
    SpiralMetricComponents,
)

__all__ = [
    # Segment density
    "Xi",
    "D_SSZ",
    "D_GR",
    "find_intersection",
    # Blend zone
    "Xi_blend",
    "Xi_complete",
    "dXi_blend_dr",
    "Xi_strong_raw",
    "Xi_weak_raw",
    "dXi_strong_raw",
    "dXi_weak_raw",
    # Metric components
    "A_Xi",
    "A_phi_series",
    "A_blended",
    "A_safe",
    "delta_M",
    "corrected_r_s",
    "metric_tensor",
    # Constants
    "PHI",
    "C",
    "G",
    "M_SUN",
    "R_SUN",
    "X_BLEND_MIN",
    "X_BLEND_MAX",
    # Advanced: Rotating Kerr-SSZ Metric
    "KerrSSZMetric",
    "KerrMetricComponents",
    "segment_density_N",
    # Advanced: Curvature Tensor Engine
    "christoffel_numerical",
    "riemann_numerical",
    "ricci_numerical",
    "einstein_numerical",
    "symbolic_curvature_diagonal",
    # Advanced: Unified Observables API
    "ObservableType",
    "SSZObservableSuite",
    # Advanced: 2PN Calibration
    "phi_g_squared",
    "phi_g",
    "gamma_factor",
    "beta_factor",
    "dtau_dt",
    "PhiSpiralSSZMetric",
    "SpiralMetricComponents",
]
