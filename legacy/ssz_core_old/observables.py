"""
SSZ Unified Observables Suite

Implements Postulate 5: "Observable -> Method Assignment"
"Never use a single method for all observables."

Observable assignments:
- Timelike (clocks, redshift) -> Xi-based: D = 1 / (1 + Xi)
- Null (light: lensing, Shapiro) -> PPN-based: (1 + gamma)
- Orbit (perihelion precession) -> PPN beta/gamma machinery

© 2025 Carmen N. Wrede & Lino Casu
Licensed under the Anti-Capitalist Software License v1.4
"""

import numpy as np
from enum import Enum
from typing import Union, Tuple, Callable

from .constants import G, C, M_SUN
from .segment_density import D_SSZ
from .blend_zone import Xi_complete


class ObservableType(str, Enum):
    TIMELIKE_REDSHIFT = "timelike_redshift"
    TIMELIKE_CLOCK = "timelike_clock"
    NULL_SHAPIRO = "null_shapiro_delay"
    NULL_LENSING = "null_light_deflection"
    TIMELIKE_PRECESSION = "timelike_orbit_precession"


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
        self.r_s = (2.0 * G * mass) / (C ** 2)
        
    def evaluate_redshift(self, r_emit: float, r_obs: float) -> float:
        """
        Gravitational redshift: 1 + z = D(r_obs) / D(r_emit)
        Uses exact Timelike direct Xi-based method (D = 1 / (1 + Xi)).
        """
        xi_emit, _, _ = Xi_complete(r_emit, self.r_s)
        xi_obs, _, _ = Xi_complete(r_obs, self.r_s)
        
        D_emit = 1.0 / (1.0 + xi_emit)
        D_obs = 1.0 / (1.0 + xi_obs)
        
        # Redshift z: 1 + z = D_obs / D_emit (since clocks run slower deeper in potential)
        return (D_obs / D_emit) - 1.0
        
    def evaluate_time_dilation(self, r: float) -> float:
        """
        Gravitational time dilation factor dτ/dt = D_SSZ(r) = 1 / (1 + Xi(r)).
        Uses exact Timelike direct Xi-based method.
        """
        xi, _, _ = Xi_complete(r, self.r_s)
        return 1.0 / (1.0 + xi)
        
    def evaluate_shapiro_delay(
        self,
        r_start: float,
        r_end: float,
        impact_param: float,
        n_points: int = 10_000
    ) -> float:
        """
        Null travel time delay (Shapiro Delay) using PPN-based integration.
        Formula: Δt_delay = (1 + γ) * (G * M / c³) * log(4 * r_start * r_end / impact_param²)
        For SSZ, γ = 1 (exact), yielding identical delay to GR.
        
        Returns:
            Shapiro time delay (seconds)
        """
        # PPN parameter gamma = 1 for SSZ (Postulate 3 & 5)
        gamma_ppn = 1.0
        
        # Standard PPN Shapiro delay formula
        factor = (1.0 + gamma_ppn) * G * self.mass / (C ** 3)
        log_term = np.log((4.0 * r_start * r_end) / (impact_param ** 2))
        
        return factor * log_term
        
    def evaluate_light_deflection(self, impact_param: float) -> float:
        """
        Light deflection angle using PPN-based lensing method.
        Formula: α = (1 + γ) * (2 * G * M) / (c² * b) = (1 + γ) * r_s / (2 * b)
        Since γ = 1, α = r_s / b = 4 * G * M / (c² * b) in radians (exact standard GR).
        
        Args:
            impact_param: Nearest approach distance (meters)
            
        Returns:
            Deflection angle (radians)
        """
        # PPN parameter gamma = 1 for SSZ
        gamma_ppn = 1.0
        
        return (1.0 + gamma_ppn) * self.r_s / impact_param
        
    def evaluate_perihelion_precession(self, semi_major_axis: float, eccentricity: float) -> float:
        """
        Perihelion precession per orbit using timelike orbit PPN machinery.
        Formula: δφ = 6 * π * G * M / (c² * a * (1 - e²))
        In terms of Schwarzschild radius: δφ = 3 * π * r_s / (a * (1 - e²))
        
        Args:
            semi_major_axis: Semi-major axis of the orbit (meters)
            eccentricity: Orbit eccentricity e ∈ [0, 1)
            
        Returns:
            Precession angle per revolution (radians)
        """
        if not (0.0 <= eccentricity < 1.0):
            raise ValueError(f"Eccentricity must be in [0, 1), got {eccentricity}")
            
        return (3.0 * np.pi * self.r_s) / (semi_major_axis * (1.0 - eccentricity ** 2))
