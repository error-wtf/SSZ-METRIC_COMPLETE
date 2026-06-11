"""
SSZ Unified Observables Suite

Implements the Prime Directive from ssz-complete-documentation:
"Observable -> Class -> Method -> Scope -> Then calculate"

Observable assignments:
- Timelike Static Clocks & Redshift (TIMELIKE_STATIC) -> Xi-based directly.
- Null light-path (NULL_LIGHT) -> PPN-based completion (factor = 1 + gamma_ppn).
- Timelike orbits (TIMELIKE_ORBIT) -> PPN orbit machinery.

No GR, Schwarzschild, or Kerr Boyer-Lindquist scaffolds are imported
or used inside this module.

© 2025 Carmen N. Wrede & Lino Casu
Licensed under the Anti-Capitalist Software License v1.4
"""

import numpy as np
from enum import Enum
from typing import Union, Tuple, Callable

from .constants import G, C, M_SUN
from .core import xi_canonical, D_from_xi, s_from_xi, characteristic_radius


class ObservableClass(str, Enum):
    NULL_LIGHT = "null_light"
    TIMELIKE_STATIC = "timelike_static"
    TIMELIKE_ORBIT = "timelike_orbit"


class MethodAssignment(str, Enum):
    PPN_COMPLETION = "ppn_completion"
    XI_DIRECT = "xi_direct"
    PPN_ORBIT = "ppn_orbit"


def classify_observable(name: str) -> ObservableClass:
    """
    Classify an observable into its canonical class per ssz-complete-documentation.
    """
    n = name.lower().strip()
    if any(k in n for k in ["lensing", "shapiro", "vlbi", "group_delay", "delay"]):
        return ObservableClass.NULL_LIGHT
    elif any(k in n for k in ["redshift", "dilation", "dilation", "gps", "clock", "pound"]):
        return ObservableClass.TIMELIKE_STATIC
    elif any(k in n for k in ["perihelion", "orbit", "precession", "dragging"]):
        return ObservableClass.TIMELIKE_ORBIT
    else:
        raise ValueError(f"Unknown physical observable: {name}")


def method_for_observable(obs_class: ObservableClass) -> MethodAssignment:
    """
    Route the canonical method assignment for the observable class.
    """
    if obs_class == ObservableClass.NULL_LIGHT:
        return MethodAssignment.PPN_COMPLETION
    elif obs_class == ObservableClass.TIMELIKE_STATIC:
        return MethodAssignment.XI_DIRECT
    elif obs_class == ObservableClass.TIMELIKE_ORBIT:
        return MethodAssignment.PPN_ORBIT
    else:
        raise ValueError(f"Unknown observable class: {obs_class}")


class SSZObservableSuite:
    """
    Unified API for evaluating physical observables according to SSZ Postulate 5.
    Guarantees correct formula and method assignment.
    """
    def __init__(self, mass: float = M_SUN):
        """
        Initialize the observables suite for a gravitating body.
        
        Args:
            mass: Mass of the body (kg)
        """
        self.mass = mass
        self.r_s = characteristic_radius(mass)
        
    def evaluate_redshift(self, r_emit: float, r_obs: float) -> float:
        """
        Gravitational redshift: f_obs / f_emit = D(r_emit) / D(r_obs)
        Uses exact TIMELIKE_STATIC direct Xi-based method (D = 1 / (1 + Xi)).
        """
        xi_emit = xi_canonical(r_emit, self.mass)
        xi_obs = xi_canonical(r_obs, self.mass)
        
        D_emit = D_from_xi(xi_emit)
        D_obs = D_from_xi(xi_obs)
        
        # Redshift z: 1 + z = D_obs / D_emit
        return float(D_obs / D_emit - 1.0)
        
    def evaluate_time_dilation(self, r: float) -> float:
        """
        Gravitational time dilation factor dτ/dt = D(r) = 1 / (1 + Xi(r)).
        Uses exact TIMELIKE_STATIC direct Xi-based method.
        """
        xi = xi_canonical(r, self.mass)
        return float(D_from_xi(xi))
        
    def null_ppn_completion(self, xi_only_result: float, gamma_ppn: float = 1.0) -> float:
        """
        PPN completion for NULL_LIGHT observables.
        Formula:
            Result = xi_only_result * (1 + gamma_ppn)
        """
        return xi_only_result * (1.0 + gamma_ppn)
        
    def evaluate_shapiro_delay(
        self,
        r_start: float,
        r_end: float,
        impact_param: float
    ) -> float:
        """
        Null travel time delay (Shapiro Delay) using PPN-based integration.
        For SSZ, gamma_ppn = 1 (exact), yielding identical delay to GR.
        
        Returns:
            Shapiro time delay (seconds)
        """
        # PPN parameter gamma = 1 for SSZ
        gamma_ppn = 1.0
        
        # Standard temporal piece (Xi-only)
        xi_only_delay = G * self.mass / (C ** 3) * np.log((4.0 * r_start * r_end) / (impact_param ** 2))
        
        # PPN completion (1 + gamma)
        return self.null_ppn_completion(xi_only_delay, gamma_ppn)
        
    def evaluate_light_deflection(self, impact_param: float) -> float:
        """
        Light deflection angle using PPN-based lensing method.
        Since gamma = 1, α = 2 * r_s / b in radians.
        
        Args:
            impact_param: Nearest approach distance (meters)
            
        Returns:
            Deflection angle (radians)
        """
        # PPN parameter gamma = 1 for SSZ
        gamma_ppn = 1.0
        
        xi_only_deflection = self.r_s / (2.0 * impact_param)
        return self.null_ppn_completion(xi_only_deflection, gamma_ppn)
        
    def evaluate_perihelion_precession(self, semi_major_axis: float, eccentricity: float) -> float:
        """
        Perihelion precession per orbit using timelike orbit PPN machinery.
        Formula: δφ = 3 * π * r_s / (a * (1 - e²))
        
        Args:
            semi_major_axis: Semi-major axis of the orbit (meters)
            eccentricity: Orbit eccentricity e ∈ [0, 1)
            
        Returns:
            Precession angle per revolution (radians)
        """
        if not (0.0 <= eccentricity < 1.0):
            raise ValueError(f"Eccentricity must be in [0, 1), got {eccentricity}")
            
        return (3.0 * np.pi * self.r_s) / (semi_major_axis * (1.0 - eccentricity ** 2))
