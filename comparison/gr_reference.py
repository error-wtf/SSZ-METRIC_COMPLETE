"""
General Relativity (GR) Reference Models

This module provides standard General Relativity reference solutions for comparison
and validation purposes only.

These GR formulations are strictly isolated and are never imported by the pure
ssz_metric_pure core package.

© 2025 Carmen Wrede & Lino Casu
Licensed under the Anti-Capitalist Software License v1.4
"""

import numpy as np
from typing import Tuple, Union
from ssz_metric_pure.constants import G, C

def Schwarzschild_metric_diagonal(coords: Union[Tuple, np.ndarray], M: float) -> np.ndarray:
    """
    Standard Schwarzschild diagonal metric components in GR.
    """
    T, r, theta, phi = coords
    r_s = (2.0 * G * M) / (C ** 2)
    
    # Avoid singularity
    r_safe = np.maximum(r, r_s + 1e-12)
    
    A_GR = 1.0 - r_s / r_safe
    
    g = np.zeros((4, 4))
    g[0, 0] = -A_GR * (C ** 2)
    g[1, 1] = 1.0 / A_GR
    g[2, 2] = r * r
    g[3, 3] = r * r * (np.sin(theta) ** 2)
    
    return g
