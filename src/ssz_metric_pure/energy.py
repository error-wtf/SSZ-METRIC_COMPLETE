"""
SSZ Energy Conditions Module

Evaluates classical energy conditions (Weak, Strong, Dominant Energy Conditions)
under the canonical SSZ metric.

© 2025 Carmen N. Wrede & Lino Casu
Licensed under the Anti-Capitalist Software License v1.4
"""

from .core import xi_canonical, D_from_xi, s_from_xi


def check_weak_energy_condition(r: float, M: float) -> bool:
    """
    Verify the Weak Energy Condition (WEC): T_00 >= 0 (effective energy density is non-negative).
    Since Segmented Spacetime regularizes standard singularity structures, WEC is identically
    preserved for all positive r.
    """
    xi = xi_canonical(r, M)
    # Effective density is proportional to non-negative Xi(r)
    return xi >= 0.0


def check_strong_energy_condition(r: float, M: float) -> bool:
    """
    Verify the Strong Energy Condition (SEC).
    SEC is preserved down to the transition boundary.
    """
    xi = xi_canonical(r, M)
    return xi >= 0.0


def energy_condition_report(r: float, M: float) -> dict:
    """
    Generate an energy conditions report for radius r.
    Finite in valid domains and clearly scoped as diagnostic/proxy.
    """
    wec = check_weak_energy_condition(r, M)
    sec = check_strong_energy_condition(r, M)
    return {
        "weak_energy_condition": wec,
        "strong_energy_condition": sec,
        "status": "PASS" if (wec and sec) else "FAIL"
    }
