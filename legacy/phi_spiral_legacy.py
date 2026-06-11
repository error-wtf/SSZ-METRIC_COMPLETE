"""
Legacy Phi-Spiral SSZ Metric Representation

Preserved for comparison and reference. This model uses a phi_G/cosh-first representation,
which is not purely Xi-primary.

© 2025 Carmen N. Wrede & Lino Casu
Licensed under the Anti-Capitalist Software License v1.4
"""

import numpy as np
from typing import Tuple, Optional, Callable
from dataclasses import dataclass
from ssz_metric_pure.constants import G, C

@dataclass(frozen=True)
class SpiralMetricComponents:
    """Container for φ-Spiral metric tensor components in flow coordinates."""
    g_tt: float
    g_tr: float  # Time-radial cross term (encodes spiral structure)
    g_rr: float
    g_thth: float
    g_phph: float
    phi_G: float
    beta: float
    gamma: float
    v_r: float  # Radial flow velocity v_r = c * beta
    dtau_dt: float  # Time dilation dτ/dt = sech(φ_G)


class PhiSpiralSSZMetric:
    """
    Legacy/comparison φ-Spiral SSZ Metric.
    Encodes the gravitational field as a local rotation angle φ_G(r).
    Each full 2π rotation corresponds to transitioning to a new subspace layer.
    """
    def __init__(
        self,
        mass: float,
        k: float = 1.0,
        r0: Optional[float] = None,
        phi_G_profile: Optional[Callable[[float], float]] = None
    ):
        """
        Initialize the φ-Spiral SSZ metric.
        
        Args:
            mass: Central mass (kg)
            k: Spiral rotation strength parameter
            r0: Scale radius (meters) (defaults to characteristic radius r_s)
            phi_G_profile: Optional custom profile for φ_G(r)
        """
        if mass <= 0:
            raise ValueError(f"Mass must be positive, got {mass}")
            
        self.mass = mass
        self.k = k
        self.r_s = (2.0 * G * mass) / (C ** 2)
        self.r0 = r0 if r0 is not None else self.r_s
        
        # Determine the rotation angle profile
        if phi_G_profile is not None:
            self._phi_G_func = phi_G_profile
        else:
            # Default logarithmic profile: φ_G(r) = k * log(1 + r/r0)
            self._phi_G_func = lambda r: self.k * np.log(1.0 + r / self.r0)
            
    def phi_G(self, r: float) -> float:
        """Get the local gravitational rotation angle φ_G(r)."""
        if r < 0:
            raise ValueError(f"Radius must be non-negative, got {r}")
        return self._phi_G_func(r)
        
    def dphi_G_dr(self, r: float, eps: float = 1e-6) -> float:
        """Calculate the radial derivative dφ_G/dr via finite differences."""
        r_p = r + eps
        r_m = max(0.0, r - eps)
        return (self.phi_G(r_p) - self.phi_G(r_m)) / (r_p - r_m)
        
    def subspace_layer(self, r: float) -> int:
        """Count the number of 2π rotations as subspace layer sheet number."""
        return int(np.floor(self.phi_G(r) / (2.0 * np.pi)))
        
    def beta(self, r: float) -> float:
        """Local velocity field β(r) = tanh(φ_G(r))."""
        return np.tanh(self.phi_G(r))
        
    def gamma(self, r: float) -> float:
        """Lorentz rapidity factor γ(r) = cosh(φ_G(r))."""
        return np.cosh(self.phi_G(r))
        
    def v_radial(self, r: float) -> float:
        """Spiral radial velocity v_r = c * β(r)."""
        return C * self.beta(r)
        
    def time_dilation(self, r: float) -> float:
        """Time dilation factor dτ/dt = sech(φ_G(r))."""
        return 1.0 / np.cosh(self.phi_G(r))
        
    def g_tt(self, r: float) -> float:
        """g_tt = -c² * sech²(φ_G(r))"""
        return -(C ** 2) / (np.cosh(self.phi_G(r)) ** 2)
        
    def g_tr(self, r: float) -> float:
        """g_tr = c * tanh(φ_G(r)) (enables helical/spiral geometry)"""
        return C * self.beta(r)
        
    def g_rr(self, r: float) -> float:
        """g_rr = 1.0 (constant radial component)"""
        return 1.0
        
    def g_thth(self, r: float) -> float:
        """g_θθ = r²"""
        return r * r
        
    def g_phph(self, r: float, theta: float) -> float:
        """g_φφ = r² sin²θ"""
        return r * r * (np.sin(theta) ** 2)
        
    def metric_components(self, r: float, theta: float = np.pi / 2.0) -> SpiralMetricComponents:
        """Compute all φ-spiral metric components and fields at (r, θ)."""
        return SpiralMetricComponents(
            g_tt=self.g_tt(r),
            g_tr=self.g_tr(r),
            g_rr=self.g_rr(r),
            g_thth=self.g_thth(r),
            g_phph=self.g_phph(r, theta),
            phi_G=self.phi_G(r),
            beta=self.beta(r),
            gamma=self.gamma(r),
            v_r=self.v_radial(r),
            dtau_dt=self.time_dilation(r)
        )
        
    def metric_tensor(self, r: float, theta: float = np.pi / 2.0) -> np.ndarray:
        """Get the full 4x4 metric tensor g_μν in flow (non-diagonal) form."""
        g = np.zeros((4, 4))
        g[0, 0] = self.g_tt(r)
        g[1, 1] = self.g_rr(r)
        g[2, 2] = self.g_thth(r)
        g[3, 3] = self.g_phph(r, theta)
        
        g_tr_val = self.g_tr(r)
        g[0, 1] = g_tr_val
        g[1, 0] = g_tr_val
        return g
        
    def diagonal_form_coefficients(self, r: float) -> Tuple[float, float]:
        """
        Get the exact coefficients of the transformed diagonal metric:
            ds² = -c²/γ² dT² + γ² dr²
        """
        gam = self.gamma(r)
        return -(C ** 2) / (gam ** 2), gam ** 2
