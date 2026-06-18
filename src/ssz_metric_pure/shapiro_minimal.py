"""SSZ Shapiro Delay - Minimal Implementation."""
import numpy as np
from .constants import C
from .core import xi_canonical, s_from_xi


def shapiro_ssz(r1, r2, mass, n=1000):
    """
    Calculate SSZ Shapiro delay (excess time over geometric path).

    The Shapiro delay is the additional light travel time caused by
    spacetime curvature, beyond the geometric path time.

    Formula: Δt = (1/c) ∫ Ξ(r) dr = (1/c) ∫ (s(r) - 1) dr
    """
    rs = np.linspace(r1, r2, n)
    delay = 0.0
    for i in range(n - 1):
        dr = rs[i + 1] - rs[i]
        xi = xi_canonical(rs[i], mass)
        # Shapiro delay contribution: Ξ(r)/c * dr
        delay += xi * dr / C
    return delay


__all__ = ['shapiro_ssz']
