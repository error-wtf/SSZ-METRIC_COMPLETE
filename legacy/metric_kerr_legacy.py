"""
SSZ Kerr Rotating Metric Module

Implements the rotating (Kerr-like) SSZ metric in Boyer-Lindquist-like coordinates:
    ds² = -A(r,θ)dt² + B(r,θ)dr² + C(r,θ)dθ² + D(r,θ)dφ² + 2E(r,θ)dt dφ
including frame dragging, ergosphere, horizons, and physical properties.

© 2025 Carmen Wrede & Lino Casu
Licensed under the Anti-Capitalist Software License v1.4
"""

import numpy as np
from typing import Tuple, Union
from dataclasses import dataclass

from ssz_metric_pure.constants import G, C, PHI

# Maximum segment density Ξ_max = 1 - e^(-φ) ≈ 0.80171
XI_MAX = 1.0 - np.exp(-PHI)


def segment_density_N(r: Union[float, np.ndarray], r_s: float) -> Union[float, np.ndarray]:
    """
    Segment count N(r) used for saturation in rotating spacetime.
    Formula:
        N(r) = XI_MAX * (1 - exp(-φ * r / r_s))
    """
    r_safe = np.maximum(r, 0.0)
    exponent = -PHI * r_safe / r_s
    exponent = np.clip(exponent, -100.0, 100.0)
    return XI_MAX * (1.0 - np.exp(exponent))


@dataclass(frozen=True)
class KerrMetricComponents:
    """Components of the Kerr-SSZ metric tensor."""
    g_tt: float
    g_rr: float
    g_thth: float
    g_phph: float
    g_tph: float  # Frame dragging cross term!
    A: float  # -g_tt coefficient
    B: float  # g_rr coefficient
    E: float  # g_tph coefficient


class KerrSSZMetric:
    """
    SSZ-Kerr Rotating Metric with frame dragging.
    Coordinates: (t, r, θ, φ) in Boyer-Lindquist-like system.
    """
    def __init__(self, mass: float, spin_star: float):
        """
        Initialize the Kerr-SSZ metric.
        
        Args:
            mass: Mass of the gravitating body (kg)
            spin_star: Dimensionless spin parameter a* = J c / (G M²) ∈ [0, 1)
        """
        if mass <= 0:
            raise ValueError(f"Mass must be positive, got {mass}")
        if not (0.0 <= abs(spin_star) < 1.0):
            raise ValueError(f"Spin parameter must be in [0, 1) to avoid naked singularity, got {spin_star}")
            
        self.mass = mass
        self.spin_star = spin_star
        
        # Schwarzschild radius
        self.r_s = (2.0 * G * mass) / (C ** 2)
        
        # Physical spin parameter a = spin_star * (G * M / c²)
        self.a_geom = abs(spin_star) * (G * mass) / (C ** 2)
        
    def Sigma(self, r: float, theta: float) -> float:
        """Σ(r,θ) = r² + a² cos²θ"""
        return r * r + self.a_geom * self.a_geom * np.cos(theta) ** 2
        
    def Delta(self, r: float) -> float:
        """Δ(r) = r² - r_s r + a²"""
        return r * r - self.r_s * r + self.a_geom * self.a_geom
        
    def A_coeff(self, r: float, theta: float) -> float:
        """
        A(r,θ) for rotating SSZ metric.
        Formula: A_static(r) * [Δ(r) / (r² + a²)]
        """
        N = segment_density_N(r, self.r_s)
        D_ssz = 1.0 / (1.0 + N)
        A_static = D_ssz * D_ssz
        
        Dlt = self.Delta(r)
        denom = r * r + self.a_geom * self.a_geom
        if denom < 1e-30:
            denom = 1e-30
            
        return A_static * (Dlt / denom)
        
    def g_tt(self, r: float, theta: float) -> float:
        """g_tt = -(1 - r_s r / Σ) * A(r, θ)"""
        Sig = self.Sigma(r, theta)
        A = self.A_coeff(r, theta)
        
        factor = 1.0 - self.r_s * r / max(Sig, 1e-30)
        return -A * factor
        
    def g_rr(self, r: float, theta: float) -> float:
        """g_rr = (Σ / Δ) / A(r, θ)"""
        Sig = self.Sigma(r, theta)
        Dlt = self.Delta(r)
        A = self.A_coeff(r, theta)
        
        return Sig / max(abs(Dlt), 1e-16) / max(A, 1e-16)
        
    def g_thth(self, r: float, theta: float) -> float:
        """g_θθ = Σ"""
        return self.Sigma(r, theta)
        
    def g_phph(self, r: float, theta: float) -> float:
        """g_φφ = (r² + a² + r_s r a² sin²θ / Σ) * sin²θ"""
        Sig = self.Sigma(r, theta)
        sin_th = np.sin(theta)
        
        term1 = r * r + self.a_geom * self.a_geom
        term2 = self.r_s * r * (self.a_geom ** 2) * (sin_th ** 2) / max(Sig, 1e-30)
        
        return (term1 + term2) * (sin_th ** 2)
        
    def g_tph(self, r: float, theta: float) -> float:
        """g_tφ = -r_s r a sin²θ / Σ"""
        if abs(self.a_geom) < 1e-30:
            return 0.0
            
        Sig = self.Sigma(r, theta)
        sin_th = np.sin(theta)
        
        # Multiply by C to scale to SI coordinate units for time/distance dragging
        return -self.r_s * r * self.a_geom * (sin_th ** 2) / max(Sig, 1e-30) * C
        
    def metric_tensor(self, r: float, theta: float) -> KerrMetricComponents:
        """Compute all 4x4 Kerr-SSZ metric tensor components."""
        g_tt_val = self.g_tt(r, theta)
        g_rr_val = self.g_rr(r, theta)
        g_thth_val = self.g_thth(r, theta)
        g_phph_val = self.g_phph(r, theta)
        g_tph_val = self.g_tph(r, theta)
        
        return KerrMetricComponents(
            g_tt=g_tt_val,
            g_rr=g_rr_val,
            g_thth=g_thth_val,
            g_phph=g_phph_val,
            g_tph=g_tph_val,
            A=-g_tt_val,
            B=g_rr_val,
            E=g_tph_val
        )
        
    def horizons(self) -> Tuple[float, float]:
        """Compute outer (r_+) and inner (r_-) horizons from Δ(r) = 0."""
        disc = self.r_s * self.r_s - 4.0 * (self.a_geom * self.a_geom)
        if disc < 0:
            raise ValueError("Extremal limit exceeded - naked singularity detected")
            
        r_plus = 0.5 * (self.r_s + np.sqrt(disc))
        r_minus = 0.5 * (self.r_s - np.sqrt(disc))
        return r_plus, r_minus
        
    def ergosphere(self, theta: float) -> float:
        """Compute outer boundary of ergosphere where g_tt = 0."""
        disc = self.r_s * self.r_s - 4.0 * (self.a_geom * self.a_geom) * np.cos(theta) ** 2
        return 0.5 * (self.r_s + np.sqrt(disc))
