"""SSZ Light Deflection."""
from .constants import G, C


def deflection_ssz(b, mass):
    """SSZ light deflection angle in radians."""
    r_s = 2 * G * mass / C**2
    return 2 * r_s / b


__all__ = ['deflection_ssz']
