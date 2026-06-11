"""
SSZ Phi-Lattice & Segmentation Scale Module

Implements segmentation-lattice calculations, radial indexing, operational path lengths,
and local geometric segment counting.

© 2025 Carmen Wrede & Lino Casu
Licensed under the Anti-Capitalist Software License v1.4
"""

import numpy as np
from .constants import PHI
from .core import xi_canonical, s_from_xi, D_from_xi
from .segmentation import segment_distance as core_segment_distance


def phi_lattice_points(k_min: int, k_max: int) -> np.ndarray:
    """
    Generate phi-lattice radial coordinates scaling exponentially with phi.
    r_k = PHI^k
    """
    indices = np.arange(k_min, k_max + 1)
    return PHI ** indices


def segment_index_from_radius(r: float, r0: float = 1.0) -> float:
    """
    Invert lattice equation to get index k for a given radius:
    k = log_PHI(r / r0)
    """
    return float(np.log(r / r0) / np.log(PHI))


def radius_from_segment_index(k: float, r0: float = 1.0) -> float:
    """
    Get lattice coordinate radius for index k:
    r = r0 * PHI^k
    """
    return float(r0 * (PHI ** k))


def segment_density_profile(r_values, M: float) -> np.ndarray:
    """
    Evaluate the primary segmentation density field Xi(r) over a radial array.
    """
    return np.array(xi_canonical(r_values, M))


def segment_distance(r1: float, r2: float, M: float) -> float:
    """
    Calculate the operational radial path length (segment distance rho) between r1 and r2.
    Uses the exact integrated radial stretching factor s(r) dr.
    """
    return float(core_segment_distance(r1, r2, M))


def segment_count_proxy(r1: float, r2: float, M: float, ell0: float = 1.0) -> float:
    """
    Return proxy segment count between r1 and r2 given base segment length scale ell0.
    N = rho(r1, r2) / ell0
    """
    rho = segment_distance(r1, r2, M)
    return float(rho / ell0)
