"""
Engineering Feasibility for SSZ Metric Applications

Device simulation, tolerances, and error budgets for practical implementation.
Focus on quantum computing and precision measurement applications.

© 2025 Carmen N. Wrede & Lino Casu
Licensed under the Anti-Capitalist Software License v1.4
"""

import numpy as np
from typing import Dict, List, Tuple, Optional, Callable
from dataclasses import dataclass
from .constants import C, G, HBAR, M_EARTH, R_EARTH
from .core import xi_canonical, D_from_xi


@dataclass
class DeviceSpec:
    """Specifications for a device operating with SSZ effects."""
    name: str
    device_type: str  # "qubit", "clock", "interferometer", "sensor"
    operating_height: float  # m above Earth surface
    precision_requirement: float  # Relative precision needed
    coherence_time: float  # s
    physical_size: float  # m (device spatial extent)


@dataclass
class ToleranceAnalysis:
    """Tolerance requirements for device operation."""
    device: DeviceSpec
    max_height_variation: float  # m
    max_xi_gradient: float  # per meter
    timing_tolerance: float  # s
    phase_tolerance: float  # rad
    passes_requirement: bool


@dataclass
class ErrorBudget:
    """Complete error budget for SSZ-sensitive device."""
    device: DeviceSpec
    ssz_contribution: float  # Error from SSZ effects
    thermal_contribution: float
    vibrational_contribution: float
    electromagnetic_contribution: float
    total_error: float
    ssz_correctable: bool  # Can SSZ error be corrected?


@dataclass
class FeasibilityResult:
    """Overall feasibility assessment."""
    device: DeviceSpec
    tolerances: ToleranceAnalysis
    error_budget: ErrorBudget
    engineering_confidence: float  # 0-1 scale
    ready_for_prototype: bool
    recommendations: List[str]


class QuantumDeviceSimulator:
    """
    Simulates quantum devices (qubits, clocks) in SSZ spacetime.
    """
    
    def __init__(self, device: DeviceSpec):
        self.device = device
        self.D_factor = D_from_xi(xi_canonical(
            R_EARTH + device.operating_height, M_EARTH
        ))
        
    def gate_timing_correction(self, nominal_time: float) -> float:
        """
        Compute corrected gate timing accounting for SSZ time dilation.
        
        t_corrected = t_nominal / D(h)
        
        Args:
            nominal_time: Intended gate time (s)
            
        Returns:
            Corrected gate time (s)
        """
        return nominal_time / self.D_factor
    
    def phase_accumulation(self, frequency: float, duration: float) -> float:
        """
        Compute phase accumulation with SSZ correction.
        
        Δφ = 2πf × t × D(h)
        
        Args:
            frequency: Qubit/clock frequency (Hz)
            duration: Operation duration (s)
            
        Returns:
            Phase in radians
        """
        return 2 * np.pi * frequency * duration * self.D_factor
    
    def coherence_limit(self) -> float:
        """
        Estimate coherence time limit from SSZ effects.
        
        Returns:
            Maximum coherence time (s)
        """
        # SSZ-induced dephasing rate
        # For 1 mm height difference across device
        delta_h = self.device.physical_size
        delta_xi = xi_canonical(
            R_EARTH + self.device.operating_height + delta_h, M_EARTH
        ) - xi_canonical(
            R_EARTH + self.device.operating_height, M_EARTH
        )
        
        # Dephasing time ~ 1 / (ω × ΔD)
        # Assume 5 GHz qubit frequency
        omega = 2 * np.pi * 5e9  # rad/s
        delta_D = delta_xi / (1 + xi_canonical(R_EARTH + self.device.operating_height, M_EARTH))**2
        
        tau_dephase = 1.0 / (omega * abs(delta_D))
        
        return min(self.device.coherence_time, tau_dephase)
    
    def height_sensitivity(self) -> float:
        """
        Compute fractional frequency shift per meter height change.
        
        Returns:
            Sensitivity (fraction per meter)
        """
        h = self.device.operating_height
        # Use larger epsilon for Earth-scale calculations to avoid numerical issues
        eps = 1.0  # 1 meter perturbation for Earth surface
        
        D1 = D_from_xi(xi_canonical(R_EARTH + h, M_EARTH))
        D2 = D_from_xi(xi_canonical(R_EARTH + h + eps, M_EARTH))
        
        sensitivity = abs(D2 - D1) / (D1 * eps)
        # Ensure minimum sensitivity for numerical stability
        return max(sensitivity, 1e-20)


def analyze_tolerances(device: DeviceSpec) -> ToleranceAnalysis:
    """
    Determine tolerance requirements for device operation.
    
    Args:
        device: Device specifications
        
    Returns:
        ToleranceAnalysis with requirements
    """
    simulator = QuantumDeviceSimulator(device)
    
    # Height variation tolerance
    # Must not exceed precision requirement
    sens = simulator.height_sensitivity()
    max_dh = device.precision_requirement / sens if sens > 0 else np.inf
    
    # Xi gradient tolerance
    xi_at_h = xi_canonical(R_EARTH + device.operating_height, M_EARTH)
    xi_at_h_plus = xi_canonical(R_EARTH + device.operating_height + device.physical_size, M_EARTH)
    xi_gradient = abs(xi_at_h_plus - xi_at_h) / device.physical_size
    
    # Timing tolerance
    # Gate timing must be precise to D(h) accuracy
    timing_tol = device.precision_requirement / (1.0 / device.coherence_time)
    
    # Phase tolerance
    phase_tol = 2 * np.pi * device.precision_requirement
    
    # Check if feasible
    # Typical lab conditions: height stable to 1 mm
    typical_height_stability = 0.001  # m
    passes = max_dh >= typical_height_stability
    
    return ToleranceAnalysis(
        device=device,
        max_height_variation=max_dh,
        max_xi_gradient=xi_gradient,
        timing_tolerance=timing_tol,
        phase_tolerance=phase_tol,
        passes_requirement=passes
    )


def compute_error_budget(device: DeviceSpec) -> ErrorBudget:
    """
    Compute complete error budget including SSZ effects.
    
    Args:
        device: Device specifications
        
    Returns:
        ErrorBudget with all contributions
    """
    simulator = QuantumDeviceSimulator(device)
    
    # SSZ contribution: Uncorrected height variations
    sens = simulator.height_sensitivity()
    # Assume 1 mm height uncertainty
    height_uncertainty = 0.001  # m
    ssz_error = sens * height_uncertainty
    
    # Thermal contribution (typical for cryogenic systems)
    # ~10^-6 relative error from temperature fluctuations
    thermal_error = 1e-6
    
    # Vibrational (isolated lab)
    # ~10^-8 relative error
    vibrational_error = 1e-8
    
    # Electromagnetic (shielded)
    # ~10^-9 relative error
    em_error = 1e-9
    
    # Total error (RSS combination)
    total = np.sqrt(ssz_error**2 + thermal_error**2 + vibrational_error**2 + em_error**2)
    
    # SSZ correctable if we can measure height to 0.1 mm
    ssz_correctable = height_uncertainty < 0.0001  # 0.1 mm
    
    return ErrorBudget(
        device=device,
        ssz_contribution=ssz_error,
        thermal_contribution=thermal_error,
        vibrational_contribution=vibrational_error,
        electromagnetic_contribution=em_error,
        total_error=total,
        ssz_correctable=ssz_correctable
    )


def assess_feasibility(device: DeviceSpec) -> FeasibilityResult:
    """
    Complete feasibility assessment for a device.
    
    Args:
        device: Device specifications
        
    Returns:
        FeasibilityResult with recommendations
    """
    tolerances = analyze_tolerances(device)
    errors = compute_error_budget(device)
    
    # Engineering confidence score
    confidence_factors = [
        1.0 if tolerances.passes_requirement else 0.5,
        1.0 if errors.ssz_correctable else 0.7,
        1.0 if errors.total_error < device.precision_requirement else 0.3,
        1.0 if device.operating_height < 1000 else 0.8  # Lower is better for SSZ
    ]
    confidence = np.mean(confidence_factors)
    
    # Ready for prototype? (convert numpy bool to Python bool)
    ready = bool(
        tolerances.passes_requirement and
        errors.total_error < device.precision_requirement * 10 and  # Within order of magnitude
        confidence > 0.7
    )
    
    # Recommendations
    recs = []
    if not tolerances.passes_requirement:
        recs.append(f"Improve height stabilization to < {tolerances.max_height_variation*1000:.1f} mm")
    if not errors.ssz_correctable:
        recs.append("Implement active height monitoring for SSZ correction")
    if device.operating_height > 1000:
        recs.append("Consider lower altitude installation for reduced SSZ effects")
    if errors.total_error > device.precision_requirement:
        recs.append("Improve thermal/vibrational isolation")
    
    return FeasibilityResult(
        device=device,
        tolerances=tolerances,
        error_budget=errors,
        engineering_confidence=confidence,
        ready_for_prototype=ready,
        recommendations=recs
    )


def simulate_qubit_array(
    num_qubits: int,
    base_height: float,
    qubit_spacing: float,
    operation_time: float
) -> Dict:
    """
    Simulate multi-qubit system with SSZ effects.
    
    Args:
        num_qubits: Number of qubits in array
        base_height: Height of first qubit (m)
        qubit_spacing: Physical spacing between qubits (m)
        operation_time: Gate operation time (s)
        
    Returns:
        Simulation results
    """
    heights = base_height + np.arange(num_qubits) * qubit_spacing
    
    # Each qubit experiences different D(h)
    D_factors = [D_from_xi(xi_canonical(R_EARTH + h, M_EARTH)) for h in heights]
    
    # Maximum timing mismatch
    timing_mismatch = max(D_factors) / min(D_factors) - 1.0
    
    # Phase difference after operation
    # Assume 5 GHz qubits
    freq = 5e9
    phases = [2 * np.pi * freq * operation_time * D for D in D_factors]
    phase_spread = max(phases) - min(phases)
    
    # Coherent zone calculation
    # How close must qubits be for phase coherence?
    # Tolerance 10^-6 relative phase
    max_dh = 1e-6 / (xi_canonical(R_EARTH + base_height, M_EARTH) * 
                     (C**2 / (G * M_EARTH)))  # Approximate
    
    return {
        'num_qubits': num_qubits,
        'heights': heights,
        'D_factors': D_factors,
        'max_timing_mismatch': timing_mismatch,
        'phase_spread': phase_spread,
        'coherent_spacing': max_dh,
        'requires_correction': timing_mismatch > 1e-9
    }


def gate_fidelity_estimate(
    device: DeviceSpec,
    num_gates: int,
    gate_time: float,
    with_ssz_correction: bool = True
) -> Dict:
    """
    Estimate quantum gate fidelity with/without SSZ correction.
    
    Args:
        device: Device specifications
        num_gates: Number of gates in circuit
        gate_time: Single gate duration (s)
        with_ssz_correction: Whether SSZ corrections applied
        
    Returns:
        Fidelity estimates
    """
    simulator = QuantumDeviceSimulator(device)
    
    # Base error rate (thermal, etc.)
    base_error = 1e-4
    
    # SSZ-induced error
    if with_ssz_correction:
        # Corrected to height measurement precision
        ssz_error = compute_error_budget(device).ssz_contribution * 0.1  # 10x better
    else:
        ssz_error = compute_error_budget(device).ssz_contribution
    
    # Per-gate error
    per_gate_error = base_error + ssz_error
    
    # Total circuit fidelity
    fidelity = (1 - per_gate_error) ** num_gates
    
    # Improvement with correction
    fidelity_uncorrected = (1 - base_error - compute_error_budget(device).ssz_contribution) ** num_gates
    
    return {
        'fidelity_per_gate': 1 - per_gate_error,
        'circuit_fidelity': fidelity,
        'fidelity_uncorrected': fidelity_uncorrected,
        'improvement_factor': fidelity / fidelity_uncorrected if fidelity_uncorrected > 0 else 1.0,
        'num_gates': num_gates,
        'ssz_corrected': with_ssz_correction
    }


def device_comparison(
    devices: List[DeviceSpec]
) -> Dict:
    """
    Compare feasibility of multiple device concepts.
    
    Args:
        devices: List of device specifications
        
    Returns:
        Comparison results
    """
    results = []
    for device in devices:
        feas = assess_feasibility(device)
        results.append({
            'name': device.name,
            'type': device.device_type,
            'confidence': feas.engineering_confidence,
            'ready': feas.ready_for_prototype,
            'total_error': feas.error_budget.total_error,
            'recommendations': len(feas.recommendations)
        })
    
    # Rank by confidence
    ranked = sorted(results, key=lambda x: x['confidence'], reverse=True)
    
    return {
        'num_devices': len(devices),
        'ranked_devices': ranked,
        'ready_count': sum(1 for r in results if r['ready']),
        'best_candidate': ranked[0]['name'] if ranked else None
    }


def generate_engineering_report(
    devices: List[DeviceSpec],
    output_path: str = "reports/engineering_feasibility_report.md"
) -> str:
    """
    Generate comprehensive engineering feasibility report.
    
    Args:
        devices: Devices to analyze
        output_path: Where to write report
        
    Returns:
        Report content
    """
    comparison = device_comparison(devices)
    
    report = f"""# SSZ Engineering Feasibility Report

**Generated:** Engineering Analysis  
**Devices Analyzed:** {len(devices)}

## Executive Summary

| Device | Type | Confidence | Prototype Ready | Total Error |
|--------|------|------------|-----------------|-------------|
"""
    
    for dev in devices:
        feas = assess_feasibility(dev)
        status = "✓" if feas.ready_for_prototype else "○"
        report += f"| {dev.name} | {dev.device_type} | "
        report += f"{feas.engineering_confidence*100:.0f}% | {status} | "
        report += f"{feas.error_budget.total_error:.2e} |\n"
    
    report += f"""
## Best Candidate: {comparison['best_candidate']}

## Detailed Analysis

"""
    
    for dev in devices:
        feas = assess_feasibility(dev)
        report += f"""### {dev.name}

**Specifications:**
- Type: {dev.device_type}
- Operating Height: {dev.operating_height} m
- Precision Required: {dev.precision_requirement:.2e}
- Coherence Time: {dev.coherence_time} s
- Physical Size: {dev.physical_size} m

**Tolerance Analysis:**
- Max Height Variation: {feas.tolerances.max_height_variation*1000:.3f} mm
- Xi Gradient: {feas.tolerances.max_xi_gradient:.2e} m⁻¹
- Timing Tolerance: {feas.tolerances.timing_tolerance:.2e} s
- Phase Tolerance: {feas.tolerances.phase_tolerance:.2e} rad

**Error Budget:**
- SSZ Contribution: {feas.error_budget.ssz_contribution:.2e}
- Thermal: {feas.error_budget.thermal_contribution:.2e}
- Vibrational: {feas.error_budget.vibrational_contribution:.2e}
- Electromagnetic: {feas.error_budget.electromagnetic_contribution:.2e}
- **Total:** {feas.error_budget.total_error:.2e}

**Recommendations:**
"""
        for rec in feas.recommendations:
            report += f"- {rec}\n"
        
        report += f"\n**Status:** {'Ready for Prototype' if feas.ready_for_prototype else 'Needs Development'}\n\n"
    
    report += """## Conclusion

The SSZ metric presents measurable but correctable effects for precision 
quantum devices. With proper height monitoring and timing corrections, 
SSZ effects can be compensated to enable next-generation quantum computing 
and timing applications.
"""
    
    # Write to file
    import os
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w') as f:
        f.write(report)
    
    return report


# Example device specifications for testing
EXAMPLE_QUBIT_DEVICE = DeviceSpec(
    name="Superconducting Qubit Array",
    device_type="qubit",
    operating_height=100.0,  # 100m above sea level
    precision_requirement=1e-6,  # 1 ppm
    coherence_time=100e-6,  # 100 microseconds
    physical_size=0.01  # 1 cm chip
)

EXAMPLE_OPTICAL_CLOCK = DeviceSpec(
    name="Strontium Optical Clock",
    device_type="clock",
    operating_height=50.0,
    precision_requirement=1e-18,  # Ultimate precision
    coherence_time=1.0,  # 1 second
    physical_size=0.5  # 50 cm vacuum chamber
)

EXAMPLE_SENSOR = DeviceSpec(
    name="Gravimetric Quantum Sensor",
    device_type="sensor",
    operating_height=200.0,
    precision_requirement=1e-8,
    coherence_time=10e-3,  # 10 ms
    physical_size=0.1  # 10 cm
)
