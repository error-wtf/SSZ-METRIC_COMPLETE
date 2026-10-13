"""SSZ Shapiro Delay - Minimal Implementation."""
import numpy as np
from .constants import C
from .core import xi_canonical, s_from_xi


def shapiro_ssz(r1, r2, mass, n=1000):
    """
    Calculate SSZ Shapiro delay (excess time over flat-space geometric path).

    Metric ds^2 = -c^2 dt^2 / s^2 + ... with s = 1 + Xi(r) gives, for a null
    ray, dt = s^2 dr / c (radial leg; the same integrand governs the full
    geodesic to leading order in Xi for a tangential ray). The EXCESS over
    the flat path is therefore

        dt_total = (1/c) * Integral (s^2 - 1) dr = (1/c) * Integral (2 Xi + Xi^2) dr

    FORENSIC AUDIT NOTE: the previous version integrated only Xi dr (i.e.
    s - 1), which is the FIRST-ORDER-ONLY term and misses the Xi^2 piece;
    against the exact metric integral this yields ~ -50% (factor 0.4863
    measured at r in [2.3, 100] r_s, matching the Phase-A audit finding).
    The exact implementation lives in shapiro_exact.py; this minimal
    version now uses the same integrand (2 Xi + Xi^2).
    """
    rs = np.linspace(r1, r2, n)
    delay = 0.0
    for i in range(n - 1):
        dr = rs[i + 1] - rs[i]
        xi = xi_canonical(rs[i], mass)
        # Shapiro delay contribution: (2 Xi + Xi^2)/c * dr
        delay += (2.0 * xi + xi * xi) * dr / C
    return delay


__all__ = ['shapiro_ssz']
