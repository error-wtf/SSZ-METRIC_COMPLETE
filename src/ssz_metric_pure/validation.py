"""
SSZ Validation Module

Contains verification utilities for the pure SSZ metric and its axiomatic foundation.

© 2025 Carmen N. Wrede & Lino Casu
Licensed under the Anti-Capitalist Software License v1.4
"""

import numpy as np
from .core import xi_canonical, D_from_xi, s_from_xi

def verify_algebraic_coupling(r: float, M: float) -> float:
    """
    Verify the fundamental axiomatic identity D(Xi) * s(Xi) == 1.
    """
    xi = xi_canonical(r, M)
    D = D_from_xi(xi)
    s = s_from_xi(xi)
    return float(D * s)


def validate_core_identities(r: float, M: float) -> bool:
    """
    Validate core algebraic and determinant identities at radius r.
    """
    coupling = verify_algebraic_coupling(r, M)
    return bool(np.isclose(coupling, 1.0, rtol=1e-12, atol=1e-12))
