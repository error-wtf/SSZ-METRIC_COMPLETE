"""
SSZ Frequency Framework Module

Implements the frequency, clock comparison, and wave phase transport
regimes of Segmented Spacetime (SSZ).

© 2025 Carmen Wrede & Lino Casu
Licensed under the Anti-Capitalist Software License v1.4
"""

import numpy as np
from .core import xi_canonical, D_from_xi


def clock_comparison_ratio(r1: float, r2: float, M: float) -> float:
    """
    Compute the comparative clock rate ratio between an observer at r1 and r2.
    Formula:
        f(r1) / f(r2) = D(r2) / D(r1) = (1 + Xi(r1)) / (1 + Xi(r2))
    """
    xi1 = xi_canonical(r1, M)
    xi2 = xi_canonical(r2, M)
    D1 = D_from_xi(xi1)
    D2 = D_from_xi(xi2)
    return float(D2 / D1)


def frequency_ratio(r1: float, r2: float, M: float) -> float:
    """
    Alias for clock_comparison_ratio.
    """
    return clock_comparison_ratio(r1, r2, M)


def phase_accumulation_radial(r1: float, r2: float, frequency: float, M: float) -> float:
    """
    Calculate the radial wave phase accumulation during propagation.
    Integrated phase of the wave from r1 to r2 is proportional to frequency and travel time.
    """
    if r1 > r2:
        r1, r2 = r2, r1
    
    # We sample the path
    r_vals = np.linspace(r1, r2, 1000)
    # n(r) = s(r)/D(r) = (1+Xi)**2
    n_vals = (1.0 + xi_canonical(r_vals, M)) ** 2
    
    # Phase delta = integral(omega * n(r) / c * dr)
    # Let's return the normalized integral: integral(n(r) dr)
    return float(np.trapezoid(n_vals, r_vals))
