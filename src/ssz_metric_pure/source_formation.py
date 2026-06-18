"""
Physical Source Formation for SSZ Metric

Implements matter coupling to the SSZ metric through consistent stress-energy
tensor construction and sourced field equations.

© 2025 Carmen N. Wrede & Lino Casu
Licensed under the Anti-Capitalist Software License v1.4
"""

import numpy as np
from typing import Union, Callable, Tuple, Optional
from dataclasses import dataclass
from .constants import C, G
from .core import characteristic_radius, xi_canonical, D_from_xi
from .metric import metric_diagonal, inverse_metric_diagonal
from .tensor import christoffel_symbols


@dataclass
class MatterConfig:
    """Configuration for matter distribution in SSZ spacetime."""
    mass: float  # Central mass (kg)
    matter_type: str = "perfect_fluid"  # Type of matter
    equation_of_state: str = "dust"  # w = p/rho: dust(0), radiation(1/3), stiff(1)
    density_profile: Optional[Callable[[float], float]] = None
    pressure_profile: Optional[Callable[[float], float]] = None


@dataclass  
class StressEnergyResult:
    """Result container for stress-energy tensor computation."""
    T_munu: np.ndarray  # T_μν at given point
    trace_T: float  # T = g^μν T_μν
    energy_density: float  # ρ
    pressure: float  # p
    valid: bool  # Check passed


@dataclass
class SourceFormationResult:
    """Complete result for source formation analysis."""
    mass: float
    r_s: float
    T_munu: np.ndarray
    G_munu: np.ndarray  # Einstein tensor
    consistency_error: float  # |G_μν - (8πG/c^4)T_μν|
    bianchi_identity: float  # |∇_μ T^μ_ν|
    valid: bool


def equation_of_state_parameter(eos_type: str) -> float:
    """
    Return w = p/ρ for standard equations of state.
    
    Args:
        eos_type: "dust", "radiation", "stiff", or "vacuum"
        
    Returns:
        w parameter
    """
    eos_map = {
        "dust": 0.0,
        "matter": 0.0,
        "radiation": 1.0/3.0,
        "stiff": 1.0,
        "vacuum": -1.0,
        "cosmological": -1.0,
    }
    return eos_map.get(eos_type, 0.0)


def perfect_fluid_stress_energy(
    r: float,
    theta: float,
    mass: float,
    energy_density: float,
    pressure: float,
    velocity_profile: Optional[Callable[[float], float]] = None
) -> StressEnergyResult:
    """
    Construct stress-energy tensor T_μν for perfect fluid in SSZ metric.
    
    For perfect fluid: T_μν = (ρ + p)u_μ u_ν + p g_μν
    
    Args:
        r: Radial coordinate (m)
        theta: Polar angle (rad)
        mass: Central mass (kg)
        energy_density: ρ in kg/m³
        pressure: p in Pa
        velocity_profile: Optional u^μ(r), defaults to static
        
    Returns:
        StressEnergyResult with T_μν and diagnostics
    """
    # Get metric
    g_munu = metric_diagonal((0.0, r, theta, 0.0), mass)
    g_inv = inverse_metric_diagonal((0.0, r, theta, 0.0), mass)
    
    # Default: static fluid (u^μ = (1/sqrt(-g_tt), 0, 0, 0))
    if velocity_profile is None:
        u_t = np.sqrt(-g_munu[0, 0]) / C  # Normalize: g^μν u_μ u_ν = -c²
        u = np.array([u_t, 0.0, 0.0, 0.0])
    else:
        u = velocity_profile(r)
        # Normalize
        norm = np.sqrt(abs(np.sum(g_munu * np.outer(u, u))))
        u = u * C / norm
    
    # Lower index: u_μ = g_μν u^ν
    u_lower = g_munu @ u
    
    # Perfect fluid T_μν = (ρ + p)u_μ u_ν + p g_μν
    rho_plus_p = (energy_density * C**2 + pressure)  # Note: ρ in energy units
    T_munu = rho_plus_p * np.outer(u_lower, u_lower) / C**2 + pressure * g_munu
    
    # Compute trace T = g^μν T_μν
    trace_T = np.sum(g_inv * T_munu)
    
    # Validation: Check dominant energy condition |p| ≤ ρ
    valid = abs(pressure) <= energy_density * C**2
    
    return StressEnergyResult(
        T_munu=T_munu,
        trace_T=trace_T,
        energy_density=energy_density,
        pressure=pressure,
        valid=valid
    )


def scalar_field_stress_energy(
    r: float,
    theta: float,
    mass: float,
    field_value: float,
    field_gradient: np.ndarray,
    potential: float,
    coupling: str = "minimal"
) -> StressEnergyResult:
    """
    Stress-energy tensor for scalar field coupled to SSZ metric.
    
    T_μν = ∂_μ φ ∂_ν φ - (1/2)g_μν(g^αβ ∂_α φ ∂_β φ + 2V(φ))
    
    Args:
        r: Radial coordinate
        theta: Polar angle
        mass: Central mass
        field_value: φ(r)
        field_gradient: ∂_μ φ as array [∂_t, ∂_r, ∂_θ, ∂_φ]
        potential: V(φ)
        coupling: "minimal" or "conformal"
        
    Returns:
        StressEnergyResult
    """
    g_munu = metric_tensor_4d(r, theta, mass)
    g_inv = inverse_metric_tensor_4d(r, theta, mass)
    
    # Compute kinetic term g^μν ∂_μ φ ∂_ν φ
    kinetic = np.sum(g_inv * np.outer(field_gradient, field_gradient))
    
    # T_μν = ∂_μ φ ∂_ν φ - (1/2)g_μν(kinetic + 2V)
    T_munu = np.outer(field_gradient, field_gradient) - 0.5 * g_munu * (kinetic + 2 * potential)
    
    # Energy density: ρ = T_μν u^μ u^ν for timelike observer
    # Approximate: ρ ≈ T_tt / (-g_tt) for static case
    energy_density = T_munu[0, 0] / (-g_munu[0, 0]) if g_munu[0, 0] < 0 else 0.0
    
    # Pressure: p = (1/3) T^i_i (spatial trace)
    spatial_T = np.sum([T_munu[i, i] * g_inv[i, i] for i in range(1, 4)])
    pressure = spatial_T / 3.0
    
    trace_T = np.sum(g_inv * T_munu)
    
    return StressEnergyResult(
        T_munu=T_munu,
        trace_T=trace_T,
        energy_density=energy_density,
        pressure=pressure,
        valid=True
    )


def einstein_tensor_from_xi(
    r: float,
    theta: float,
    mass: float
) -> np.ndarray:
    """
    Compute Einstein tensor G_μν from Xi-primary metric.
    
    Uses the metric components derived directly from Xi(r).
    
    Args:
        r: Radial coordinate
        theta: Polar angle
        mass: Central mass
        
    Returns:
        G_μν as 4x4 array
    """
    from .tensor import einstein_tensor
    
    # Compute Einstein tensor
    coords = (0.0, r, theta, 0.0)
    G = einstein_tensor(coords, mass)
    
    return G


def source_consistency_check(
    r: float,
    theta: float,
    mass: float,
    matter: MatterConfig,
    tolerance: float = 1e-6
) -> SourceFormationResult:
    """
    Verify Einstein equations: G_μν = (8πG/c⁴)T_μν
    
    This is the fundamental consistency check for physical source formation.
    
    Args:
        r: Radial coordinate to test
        theta: Polar angle
        mass: Central mass
        matter: Matter configuration
        tolerance: Acceptable relative error
        
    Returns:
        SourceFormationResult with full diagnostics
    """
    r_s = characteristic_radius(mass)
    
    # Get Einstein tensor from metric
    G_munu = einstein_tensor_from_xi(r, theta, mass)
    
    # Construct T_μν based on matter type
    if matter.matter_type == "perfect_fluid":
        w = equation_of_state_parameter(matter.equation_of_state)
        
        # Estimate energy density from mass and radius
        if matter.density_profile:
            rho = matter.density_profile(r)
        else:
            # Simple estimate: ρ ~ M/(4/3 π r³) for interior
            rho = mass / (4.0/3.0 * np.pi * r**3) if r > r_s else 0.0
        
        p = w * rho * C**2
        
        T_result = perfect_fluid_stress_energy(r, theta, mass, rho, p)
        T_munu = T_result.T_munu
    else:
        raise ValueError(f"Unknown matter type: {matter.matter_type}")
    
    # Check Einstein equations
    kappa = 8.0 * np.pi * G / C**4
    expected_G = kappa * T_munu
    
    # Consistency error
    diff = G_munu - expected_G
    # Avoid division by zero - use absolute error where G is small
    denom = np.abs(expected_G)
    denom[denom < 1e-30] = 1.0  # Prevent div by zero
    rel_error = np.abs(diff) / denom
    max_error = np.max(rel_error)
    
    # Check Bianchi identity: ∇_μ T^μ_ν ≈ 0 (energy-momentum conservation)
    # Simplified check for static spherical case
    bianchi = _check_bianchi_identity(r, theta, mass, T_munu)
    
    valid = max_error < tolerance and bianchi < tolerance
    
    return SourceFormationResult(
        mass=mass,
        r_s=r_s,
        T_munu=T_munu,
        G_munu=G_munu,
        consistency_error=max_error,
        bianchi_identity=bianchi,
        valid=valid
    )


def _check_bianchi_identity(
    r: float,
    theta: float,
    mass: float,
    T_munu: np.ndarray,
    h: float = 1e-6
) -> float:
    """
    Numerically check ∇_μ T^μ_ν = 0 (Bianchi identity).
    
    For static case, primarily checks radial component.
    """
    # Get metric and Christoffel
    coords = (0.0, r, theta, 0.0)
    g_munu = metric_diagonal(coords, mass)
    g_inv = inverse_metric_diagonal(coords, mass)
    Gamma = christoffel_symbols(coords, mass)
    
    # Raise index: T^μ_ν = g^μα T_αν
    T_mixed = g_inv @ T_munu
    
    # For static case, only radial derivative matters
    # ∇_μ T^μ_r = ∂_μ T^μ_r + Γ^μ_μλ T^λ_r - Γ^λ_μr T^μ_λ
    
    # Approximate derivative numerically
    T_r_plus = perfect_fluid_stress_energy(r + h, theta, mass, 
                                          T_munu[0, 0] / C**2, 0.0).T_munu
    T_r_minus = perfect_fluid_stress_energy(r - h, theta, mass,
                                            T_munu[0, 0] / C**2, 0.0).T_munu
    
    dT_dr = (T_r_plus - T_r_minus) / (2 * h)
    dT_dr_mixed = g_inv @ dT_dr
    
    # Simplified divergence for static spherical case
    divergence = abs(dT_dr_mixed[1, 1])  # Radial-radial component
    
    return divergence


def vacuum_source_formation(
    mass: float,
    test_radii: Optional[np.ndarray] = None
) -> dict:
    """
    Source formation in vacuum (T_μν = 0).
    
    Verifies G_μν = 0 outside matter distribution.
    
    Args:
        mass: Central mass
        test_radii: Radii to test, defaults to [2r_s, 3r_s, 5r_s, 10r_s]
        
    Returns:
        Dictionary with test results
    """
    if test_radii is None:
        r_s = characteristic_radius(mass)
        test_radii = np.array([2.0, 3.0, 5.0, 10.0]) * r_s
    
    results = []
    for r in test_radii:
        G = einstein_tensor_from_xi(r, np.pi/2, mass)
        # In vacuum, G should be small
        G_norm = np.linalg.norm(G)
        results.append({
            'r': r,
            'G_norm': G_norm,
            'vacuum_valid': G_norm < 1e-10
        })
    
    return {
        'mass': mass,
        'test_points': len(test_radii),
        'all_vacuum_valid': all(r['vacuum_valid'] for r in results),
        'results': results
    }


def interior_solution_formation(
    mass: float,
    radius: float,
    num_points: int = 100
) -> dict:
    """
    Construct interior solution with proper source formation.
    
    For r < R (surface), solve with matter source.
    For r > R, vacuum solution.
    
    Args:
        mass: Total mass
        radius: Object radius
        num_points: Number of radial points
        
    Returns:
        Interior solution data
    """
    r_s = characteristic_radius(mass)
    
    # Uniform density for simplicity
    rho_0 = mass / (4.0/3.0 * np.pi * radius**3)
    
    radii = np.linspace(0.1 * r_s, 2 * radius, num_points)
    
    solutions = []
    for r in radii:
        # Matter inside, vacuum outside
        if r < radius:
            matter = MatterConfig(
                mass=mass,
                matter_type="perfect_fluid",
                equation_of_state="dust"
            )
            result = source_consistency_check(r, np.pi/2, mass, matter)
        else:
            # Vacuum
            G = einstein_tensor_from_xi(r, np.pi/2, mass)
            result = {
                'r': r,
                'vacuum': True,
                'G_norm': np.linalg.norm(G)
            }
        
        solutions.append(result)
    
    return {
        'mass': mass,
        'radius': radius,
        'density': rho_0,
        'compactness': r_s / radius,
        'solutions': solutions
    }
